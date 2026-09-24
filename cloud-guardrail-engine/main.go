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
	Policy    string `json:"policy"`
	Resource  string `json:"resource"`
	Passed    bool   `json:"passed"`
	Message   string `json:"message,omitempty"`
	Severity  string `json:"severity"`
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

	// Walk policy directory
	err := filepath.Walk(policyDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() || !strings.HasSuffix(info.Name(), ".rego") {
			return nil
		}

		// Read policy file
		policyContent, err := os.ReadFile(path)
		if err != nil {
			return fmt.Errorf("failed to read policy %s: %w", path, err)
		}

		// Parse and compile the policy
		compiler, err := ast.CompileModules(map[string]string{
			path: string(policyContent),
		})
		if err != nil {
			return fmt.Errorf("failed to compile policy %s: %w", path, err)
		}

		// Evaluate the policy against the input
		regoQuery := rego.New(
			rego.Query("data"),
			rego.Compiler(compiler),
			rego.Input(input),
		)

		rs, err := regoQuery.Eval(ctx)
		if err != nil {
			return fmt.Errorf("failed to evaluate policy %s: %w", path, err)
		}

		// Process results
		results := processResults(path, rs)
		report.Results = append(report.Results, results...)
		report.TotalPolicies++

		return nil
	})

	if err != nil {
		return nil, err
	}

	// Count passed/failed
	for _, r := range report.Results {
		if r.Passed {
			report.Passed++
		} else {
			report.Failed++
		}
	}

	return report, nil
}

func processResults(policyPath string, rs rego.ResultSet) []PolicyResult {
	var results []PolicyResult

	for _, result := range rs {
		for _, expr := range result.Expressions {
			if data, ok := expr.Value.(map[string]interface{}); ok {
				if violations, exists := data["violation"]; exists {
					if violationList, ok := violations.([]interface{}); ok {
						for _, v := range violationList {
							if vMap, ok := v.(map[string]interface{}); ok {
								results = append(results, PolicyResult{
									Policy:   filepath.Base(policyPath),
									Resource: fmt.Sprintf("%v", vMap["resource"]),
									Passed:   false,
									Message:  fmt.Sprintf("%v", vMap["msg"]),
									Severity: fmt.Sprintf("%v", vMap["severity"]),
								})
							}
						}
					}
				}
			}
		}
	}

	// If no violations found, policy passed
	if len(results) == 0 {
		results = append(results, PolicyResult{
			Policy:  filepath.Base(policyPath),
			Passed:  true,
			Message: "All resources compliant",
		})
	}

	return results
}

func printReport(report *EvaluationReport) {
	fmt.Println("╔══════════════════════════════════════════════════════════╗")
	fmt.Println("║         Cloud Guardrail Engine - Evaluation Report      ║")
	fmt.Println("╠══════════════════════════════════════════════════════════╣")
	fmt.Printf("║  Total Policies: %-3d                                   ║\n", report.TotalPolicies)
	fmt.Printf("║  Passed:         %-3d                                   ║\n", report.Passed)
	fmt.Printf("║  Failed:         %-3d                                   ║\n", report.Failed)
	fmt.Println("╠══════════════════════════════════════════════════════════╣")

	for _, r := range report.Results {
		status := "✅ PASS"
		if !r.Passed {
			status = "❌ FAIL"
		}
		fmt.Printf("║  %s  %-20s %-25s ║\n", status, r.Policy, r.Resource)
		if r.Message != "" && !r.Passed {
			fmt.Printf("║         └─ %s (Severity: %s)\n", r.Message, r.Severity)
		}
	}

	fmt.Println("╚══════════════════════════════════════════════════════════╝")
}
