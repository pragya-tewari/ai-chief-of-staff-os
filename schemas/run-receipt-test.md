# Run-receipt recovery tests

An assistant or integration implements the lightweight rerun contract correctly
only if it passes all three scenarios below. These are behaviour tests: the exact
wording of a receipt may differ, but its run key, action keys and state transitions
must preserve the same safety properties.

## Scenario 1: a completed local action is not duplicated

Given a receipt whose `report` action is `succeeded` and whose destination file
still contains the expected report, when the same run key is invoked again, the
assistant reads the receipt and destination and does not create a second file or
append duplicate content. It may continue other planned or failed actions.

**Pass:** one report remains, and `report` remains `succeeded`.

**Fail:** a second report is created merely because the job was invoked again.

## Scenario 2: a failed local action is retried selectively

Given a receipt with one `succeeded` action and one `failed` local action, when the
same run key is invoked again, the assistant verifies both destinations, preserves
the succeeded action and retries only the failed action after diagnosing the
failure.

**Pass:** the succeeded action is untouched and only the failed action is retried.

**Fail:** the whole job is replayed, or the failed action is treated as if it had
succeeded without checking its destination.

## Scenario 3: an interrupted external action is verified before retry

Given a receipt whose external `send` action is still `in-progress` because the
session ended after the tool call began, when the same run key is invoked again,
the assistant changes the run to `needs-verification`, treats `send` as
`uncertain`, and checks the destination tool for an external ID or matching result.

- If the result exists, record its identifier and mark `send` `succeeded` without
  sending again.
- If the result does not exist and the tool proves that, return the action to the
  appropriate approval gate before retrying it.
- If the tool cannot prove either outcome, stop and ask the user. Do not send.

**Pass:** no second external action occurs before verification and, where needed,
fresh approval.

**Fail:** the action is blindly retried, or an ambiguous outcome is silently marked
successful.

## Concurrency boundary

Two assistants starting the same run at the same time is outside this model. The
correct response is to avoid concurrent runs; a deployment that needs concurrency
must add a lock or transactional store rather than claiming these tests provide
exactly-once execution.
