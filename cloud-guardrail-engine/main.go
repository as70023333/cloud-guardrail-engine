package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/open-policy-agent/opa/ast"
	"github.com/open-policy-agent/opa/rego"
	"github.com/spf13/cobra"
)

// PolicyResult represents the evaluation result of a single policy
type PolicyResult struct {
	Policy   string `json:"policy"`
	Package  string `json:"package"`
	Passed   bool   `json:"passed"`
	Denials  []string `json:"denials,omitempty"`
}

// EvaluationReport holds the complete evaluation results
type EvaluationReport struct {
	TotalPolicies int            `json:"total_policies"`
	Passed        int            `json:"passed"`
	Failed        int            `json:"failed"`
	Results       []PolicyResult `json:"results"`
}

var (
	policiesDir string
	planFile    string
	outputJSON  bool
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "cloud-guardrail-engine",
		Short: "Evaluate Terraform plans against cloud security policies using OPA",
		Long: `Cloud Guardrail Engine is a CLI tool that evaluates Terraform plan JSON
output against Open Policy Agent (OPA) Rego policies to enforce
cloud security guardrails before infrastructure changes are applied.`,
		RunE: runEvaluation,
	}

	rootCmd.Flags().StringVarP(&policiesDir, "policies", "p", "./policies", "Path to OPA policy directory")
	rootCmd.Flags().StringVarP(&planFile, "plan", "f", "", "Path to Terraform plan JSON file")
	rootCmd.Flags().BoolVarP(&outputJSON, "json", "j", false, "Output results as JSON")

	rootCmd.MarkFlagRequired("plan")

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func runEvaluation(cmd *cobra.Command, args []string) error {
	// Read Terraform plan
	planData, err := os.ReadFile(planFile)
	if err != nil {
		return fmt.Errorf("failed to read plan file: %w", err)
	}

	var tfPlan map[string]interface{}
	if err := json.Unmarshal(planData, &tfPlan); err != nil {
		return fmt.Errorf("failed to parse plan JSON: %w", err)
	}

	// Load and evaluate policies
	report, err := evaluatePolicies(policiesDir, tfPlan)
	if err != nil {
		return fmt.Errorf("policy evaluation failed: %w", err)
	}

	// Output results
	if outputJSON {
		output, err := json.MarshalIndent(report, "", "  ")
		if err != nil {
			return fmt.Errorf("failed to marshal report: %w", err)
		}
		fmt.Println(string(output))
	} else {
		printReport(report)
	}

	// Exit with error if any policies failed
	if report.Failed > 0 {
		return fmt.Errorf("%d policy violation(s) found", report.Failed)
	}

	return nil
}

func evaluatePolicies(policyDir string, input map[string]interface{}) (*EvaluationReport, error) {
	ctx := context.Background()
	report := &EvaluationReport{}

	// Collect all .rego files
	var policyFiles []string
	err := filepath.Walk(policyDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".rego") {
			policyFiles = append(policyFiles, path)
		}
		return nil
	})
	if err != nil {
		return nil, fmt.Errorf("failed to walk policy directory: %w", err)
	}

	if len(policyFiles) == 0 {
		return nil, fmt.Errorf("no .rego policy files found in %s", policyDir)
	}

	// Load all policies into a single compiler
	modules := make(map[string]string)
	for _, pf := range policyFiles {
		content, err := os.ReadFile(pf)
		if err != nil {
			return nil, fmt.Errorf("failed to read policy %s: %w", pf, err)
		}
		modules[pf] = string(content)
	}

	compiler, err := ast.CompileModules(modules)
	if err != nil {
		return nil, fmt.Errorf("failed to compile policies: %w", err)
	}

	// Evaluate all policies against the input
	regoQuery := rego.New(
		rego.Query("data"),
		rego.Compiler(compiler),
		rego.Input(input),
	)

	rs, err := regoQuery.Eval(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to evaluate policies: %w", err)
	}

	// Process results from each package
	for _, result := range rs {
		for _, expr := range result.Expressions {
			if data, ok := expr.Value.(map[string]interface{}); ok {
				// Navigate into nested packages (e.g., cloud -> guardrail -> aws)
				processPackageResults(data, "", report)
			}
		}
	}

	return report, nil
}

func processPackageResults(data map[string]interface{}, prefix string, report *EvaluationReport) {
	for key, value := range data {
		fullKey := key
		if prefix != "" {
			fullKey = prefix + "." + key
		}

		switch v := value.(type) {
		case map[string]interface{}:
			// Check if this is a package with deny/allow rules
			if _, hasDeny := v["deny"]; hasDeny {
				result := processPolicyResult(key, fullKey, v)
				report.Results = append(report.Results, result)
				report.TotalPolicies++
				if result.Passed {
					report.Passed++
				} else {
					report.Failed++
				}
			} else {
				// Recurse into nested packages
				processPackageResults(v, fullKey, report)
			}
		}
	}
}

func processPolicyResult(name string, pkg string, data map[string]interface{}) PolicyResult {
	result := PolicyResult{
		Policy:  name,
		Package: pkg,
		Passed:  true,
	}

	// Check for deny set
	if denyVal, exists := data["deny"]; exists {
		if denySet, ok := denyVal.([]interface{}); ok {
			for _, d := range denySet {
				if reason, ok := d.(string); ok {
					result.Denials = append(result.Denials, reason)
					result.Passed = false
				}
			}
		}
	}

	// Also check allow
	if allowVal, exists := data["allow"]; exists {
		if allowed, ok := allowVal.(bool); ok && allowed {
			result.Passed = true
			result.Denials = nil
		}
	}

	return result
}

func printReport(report *EvaluationReport) {
	fmt.Println("╔══════════════════════════════════════════════════════════════╗")
	fmt.Println("║          Cloud Guardrail Engine - Evaluation Report         ║")
	fmt.Println("╠══════════════════════════════════════════════════════════════╣")
	fmt.Printf("║  Total Policies: %-3d                                        ║\n", report.TotalPolicies)
	fmt.Printf("║  Passed:         %-3d                                        ║\n", report.Passed)
	fmt.Printf("║  Failed:         %-3d                                        ║\n", report.Failed)
	fmt.Println("╠══════════════════════════════════════════════════════════════╣")

	for _, r := range report.Results {
		status := "✅ PASS"
		if !r.Passed {
			status = "❌ FAIL"
		}
		fmt.Printf("║  %s  %-40s ║\n", status, r.Package)
		for _, d := range r.Denials {
			fmt.Printf("║         └─ %s\n", d)
		}
	}

	fmt.Println("╚══════════════════════════════════════════════════════════════╝")
}
