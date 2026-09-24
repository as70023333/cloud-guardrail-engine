package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/open-policy-agent/opa/rego"
)

// EvaluationReport holds the output of the guardrail scan
type EvaluationReport struct {
	Compliant  bool     `json:"compliant"`
	Violations []string `json:"violations"`
}

func main() {
	planPath := flag.String("plan", "", "Path to Terraform plan JSON file")
	policyDir := flag.String("policies", "./policies", "Path to directory containing Rego policies")
	flag.Parse()

	if *planPath == "" {
		fmt.Println("Usage: cloud-guardrail -plan <path-to-tfplan.json> [-policies <path>]")
		os.Exit(1)
	}

	// 1. Read Input Terraform Plan File
	inputData, err := os.ReadFile(*planPath)
	if err != nil {
		log.Fatalf("Error reading input plan file: %v", err)
	}

	var inputInterface interface{}
	if err := json.Unmarshal(inputData, &inputInterface); err != nil {
		log.Fatalf("Error parsing JSON input: %v", err)
	}

	ctx := context.Background()

	// 2. Construct OPA Query for AWS & Azure packages
	query, err := rego.New(
		rego.Query("data.cloud.guardrail"),
		rego.Load([]string{*policyDir}, nil),
	).PrepareForEval(ctx)

	if err != nil {
		log.Fatalf("Failed to initialize OPA engine: %v", err)
	}

	// 3. Evaluate Policies against Input
	results, err := query.Eval(ctx, rego.EvalInput(inputInterface))
	if err != nil {
		log.Fatalf("Policy evaluation error: %v", err)
	}

	// 4. Parse Violations
	violations := []string{}
	if len(results) > 0 && len(results[0].Expressions) > 0 {
		bindings, ok := results[0].Expressions[0].Value.(map[string]interface{})
		if ok {
			for provider, rules := range bindings {
				if providerMap, ok := rules.(map[string]interface{}); ok {
					if denyList, ok := providerMap["deny"].([]interface{}); ok {
						for _, item := range denyList {
							violations = append(violations, fmt.Sprintf("[%s] %v", provider, item))
						}
					}
				}
			}
		}
	}

	// 5. Generate Output Report
	report := EvaluationReport{
		Compliant:  len(violations) == 0,
		Violations: violations,
	}

	reportJSON, _ := json.MarshalIndent(report, "", "  ")
	fmt.Println(string(reportJSON))

	if !report.Compliant {
		os.Exit(1) // Non-zero exit code for CI/CD failure
	}
}
