# ClawPipe Orchestration E2E — Gherkin Spec

## v0.1.0 Features

### Scenario: Sequential stage execution
Given a pipeline with 5 stages in dependency order
When the pipeline runs
Then all stages execute in dependency order and complete

### Scenario: Stage retry on transient failure
Given a stage configured with max_retries: 2
When the stage command fails transiently then succeeds
Then the pipeline retries and completes

### Scenario: Approval gate pauses execution
Given a pipeline with an approval stage
When execution reaches the approval gate
Then the pipeline returns needs_approval envelope with resumeToken

### Scenario: Output contract enforcement
Given a stage with an output_contract
When the stage completes but the contract fails
Then the stage is marked failed

### Scenario: Lesson extraction from failures
Given a pipeline run with stage failures
When the run completes
Then lessons are extracted with error_signature normalization

## v0.2.0 Features

### Scenario: Reflection loop with rubric evaluation
Given a stage with type: reflection and a rubric
When the producer output passes the rubric
Then the reflection loop exits on the first iteration

### Scenario: Dynamic model routing per stage
Given stages with different reasoning_mode values
When each stage is dispatched
Then model_routed events show correct model (haiku/sonnet/opus)

### Scenario: Quality scoring post-run
Given a completed pipeline run
When quality scoring runs
Then a 5-dimension QualityScore is computed and persisted

### Scenario: Regression detection
Given a quality baseline from prior runs
When a new run scores >20% below baseline
Then regression_detected event is emitted

### Scenario: DAG dependency ordering
Given stages with diamond dependency pattern (A->[B,C]->D)
When the pipeline runs
Then B and C are dispatched after A, D waits for both

### Scenario: Opik graceful degradation
Given Opik SDK is not installed
When the pipeline runs
Then the pipeline completes without error (graceful degradation)

### Scenario: BEADS graceful degradation
Given bd CLI is not on PATH
When a stage has beads_dependency
Then the pipeline continues without blocking

## v0.3.0 Features

### Scenario: Goal evaluation post-run
Given a pipeline with goals (quality >= 0.7, completeness >= 1.0)
When the pipeline completes
Then goal_evaluated events show both goals passed

### Scenario: Mandatory audit logging
Given any pipeline run
When the run completes (success or failure)
Then an AuditEntry is written to memory/logs/audit/YYYY-MM-DD.yaml

### Scenario: Guardrail pre-run check
Given a pipeline with guardrails (stage_count <= 100)
When the pipeline starts
Then guardrail is evaluated before first stage

### Scenario: Pipeline factory generates config
Given an intent "Build a 3-email welcome sequence"
When the factory action is invoked
Then a valid pipeline config is generated with stages and agents

### Scenario: Auto-rubric generation
Given a pipeline config with stages
When rubric-gen is invoked
Then a RubricCandidate is generated with criteria
