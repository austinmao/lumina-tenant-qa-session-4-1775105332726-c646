steps:
  - id: init
    command: >-
      python3 ../../../scripts/lobster-campaign-run.py init
      --pipeline-id '${pipeline_id}'
      --campaign-slug '${campaign_slug}'
      --page-slug '${page_slug}'
      --campaign-type webinar
      --topic '${topic}'
      --event-date '${event_date}'
      --launch-date '${launch_date}'
      --orchestrator agents-campaigns-campaign-orchestrator

  - id: copy
    command: ../../../scripts/lobster-run-copywriter.sh ${pipeline_id}

  - id: save-copy-deck
    command: ../../../scripts/lobster-save-copy-deck.sh ${pipeline_id}
    stdin: $copy.stdout

  - id: email-html
    command: ../../../scripts/lobster-forge-parallel-v3.sh ${pipeline_id}

  - id: pages
    command: ../../../scripts/lobster-run-pages-v2.sh ${pipeline_id}

  - id: verify
    command: ../../../scripts/lobster-verify-campaign.sh ${pipeline_id}

  - id: brand-gate
    command: ../../../scripts/lobster-run-brand-gate-v3.sh ${pipeline_id}

  - id: brand-gate-check
    command: ../../../scripts/lobster-brand-gate-check-v2.sh ${pipeline_id}
    stdin: $brand-gate.stdout

  - id: approval
    command: cat
    stdin: $brand-gate-check.stdout
    approval: required

  - id: publish
    command: ../../../scripts/lobster-publish-campaign.sh ${pipeline_id}
    condition: $approval.approved

  - id: record-create
    command: ../../../scripts/lobster-record-create.sh ${pipeline_id}
    condition: $approval.approved
