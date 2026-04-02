---
name: gtm-implementation
description: >
  Configure a GTM container with tags, triggers, variables, and data layer
  design. Use when implementing event tracking, setting up consent mode,
  or debugging tag firing issues in Google Tag Manager.
version: "1.0.0"
permissions:
  filesystem: none
  network: true
triggers:
  - command: /gtm-implementation
metadata:
  openclaw:
    emoji: "label"
    requires:
      bins: []
      env:
        - GTM_CONTAINER_ID
---

# GTM Implementation

## Overview

Configure Google Tag Manager containers for event tracking implementation.
This skill produces GTM configuration specs: tag definitions, trigger rules,
variable mappings, data layer schemas, consent mode configuration, and
debugging procedures. It does not define the event taxonomy itself (see
`analytics-tracking` and `event-taxonomy` for that) — it translates an
existing taxonomy into GTM implementation.

## Steps

1. **Confirm container scope.** Verify the GTM container ID from
   `GTM_CONTAINER_ID`. Ask which site and event taxonomy this container
   implements. If multiple sites share a container, document the scope.

2. **Design data layer schema.** For each tracked event:
   - Define the exact `dataLayer.push()` call the site code must emit.
   - Specify all required parameters with types and example values.
   - Document which page or component triggers each push.

   ```javascript
   dataLayer.push({
     'event': 'event_name',
     'param_1': 'value',
     'param_2': 'value'
   });
   ```

3. **Create GTM variables.** For each data layer parameter:
   - Create a Data Layer Variable with the exact key name.
   - Naming convention: `DLV - [parameter_name]` (e.g., `DLV - webinar_slug`).
   - For computed values, create Custom JavaScript variables.
   - For constants (measurement ID, property ID), use Constant variables.

4. **Create GTM triggers.** For each event:
   - Create a Custom Event trigger matching the event name.
   - Naming convention: `CE - [event_name]` (e.g., `CE - quiz_completed`).
   - For page-load events, use Page View or DOM Ready triggers as appropriate.
   - For click events, use Click triggers with CSS selectors or Click ID.

5. **Create GTM tags.** For each event:
   - Create a GA4 Event tag firing on its trigger.
   - Naming convention: `GA4 - [event_name]`.
   - Map all data layer variables to GA4 event parameters.
   - Set the Measurement ID from the Constant variable.
   - Apply consent check: tag fires only when analytics consent is granted.

6. **Configure consent mode.** Set up GA4 Consent Mode v2:
   - Default state: `denied` for `analytics_storage` and `ad_storage`.
   - Update state to `granted` when user accepts cookies.
   - Ensure all GA4 tags respect consent settings via Built-In Consent Checks.
   - Document the consent management platform (CMP) integration.

7. **Organize container.** Create folders by funnel stage or functional area:
   - Each folder contains its tags, triggers, and variables.
   - Add descriptive notes to each tag explaining its purpose.

8. **Produce debugging checklist.** For each tag:
   - Expected trigger condition.
   - Expected parameter values.
   - How to verify in GTM Preview Mode.
   - How to verify in GA4 DebugView.

9. **Document version and publish notes.** Before each container publish:
   - Create a named version with a description of changes.
   - List all tags added, modified, or removed.

## Output

A **GTM Implementation Spec** with:
- Data layer schema (all events with parameters and types)
- Variable definitions table
- Trigger definitions table
- Tag definitions table (with consent checks)
- Consent mode configuration
- Container folder structure
- Debugging checklist per tag
- Publish notes template

## Error Handling

- If `GTM_CONTAINER_ID` is not set: ask the operator for the container ID
  or confirm that a new container should be created.
- If the event taxonomy is not defined yet: recommend running
  `analytics-tracking` or `event-taxonomy` first to define events before
  implementing them in GTM.
- If a data layer push is not firing: check that the site code actually
  calls `dataLayer.push()` on the expected user action, and that the GTM
  snippet is loaded before the push.
- If tags fire but parameters are empty: check that the Data Layer Variable
  name exactly matches the key in the `dataLayer.push()` call (case-sensitive).
- If consent mode blocks all tags: verify the CMP updates consent state
  correctly and that the consent signal reaches GTM.
