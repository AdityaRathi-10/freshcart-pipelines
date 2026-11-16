# FreshCart Pipelines

This repository contains the four assignment components:

- `elt/`: Snowflake-style FreshCart ELT SQL and a reproducible local notebook.
- `iris_project/`: Mage-compatible Iris classifier blocks and metadata.
- `stream/`: RabbitMQ topic-exchange dispatcher and driver.
- `tests/`: CI test for the data-preparation block.

## Local checks

```bash
python -m pip install -r requirements.txt
pytest -q
```

The RabbitMQ scripts use `RABBITMQ_URL` from the environment. Never commit that
URL; use a local broker or a secret in the execution environment.

## Guided submission sequence

Run every command from this folder. In PowerShell, use the Python interpreter
selected by VS Code. The examples below use `python`; replace it with the
selected interpreter path if `python` is not on your PATH.

### 1. Install and verify locally

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected result: `1 passed`. A warning from a third-party package is harmless
when the exit code is zero.

### 2. Create exactly five meaningful commits

Create the GitHub repository `freshcart-pipelines`, then run these commits in
order. Do not combine them into one commit.

```powershell
git init
git branch -M main
git add .gitignore requirements.txt README.md
git commit -m "chore: initialize repository configuration" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git add iris_project tests
git commit -m "feat: add tested Iris Mage pipeline" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git add .github
git commit -m "ci: run Python tests on every push" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git add stream
git commit -m "feat: add RabbitMQ dispatcher and driver" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git add elt RollNo_Name_Pipelines.pdf
git commit -m "docs: add FreshCart ELT materials and report" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Connect and push once the five local commits exist:

```powershell
git remote add origin https://github.com/<YOUR_USERNAME>/freshcart-pipelines.git
git push -u origin main
git log --oneline -5
```

Replace `<YOUR_USERNAME>` only in your local command. Do not put credentials in
the repository.

### 3. Produce the CI evidence

After the first push, open GitHub **Actions** and capture the green run. Then
make a temporary failing commit:

1. In `iris_project/transformers/prepare_data.py`, change `index % 5` to
   `index % 4`.
2. Run `python -m pytest -q` and confirm it fails.
3. Commit and push with `git commit -am "test: demonstrate failing CI gate"`.
4. Capture the red GitHub Actions run.
5. Change `% 4` back to `% 5`, run pytest again, then commit and push:
   `git commit -am "fix: restore the 80 20 data split"`.
6. Capture the final green run. This temporary demonstration commit is
   additional to the five baseline commits.

### 4. Complete Snowflake evidence

Use your own Snowflake trial account and keep secrets in Colab secrets or
environment variables. Run the baseline notebook from top to bottom. Keep the
executed baseline and the separate evidence notebooks for B2, B3, B4, and B5
under `elt/`. Record predictions before each rerun, then record actual results
and save screenshots under `elt/FreshCard_Evidence/`.

### 5. Complete Mage and RabbitMQ evidence

Run the blocks described by `iris_project/metadata.yaml`, capture the graph,
the five `max_depth` runs, the evaluation branch, confusion matrix, and
metrics. Set `RABBITMQ_URL` locally, start at least three drivers, run the
dispatcher for two minutes, and capture valid ACKs plus the tenth-message
NACK. Never commit `.env` or the broker URL.
 
### 6. Finish the report

Replace `RollNo_Name` with your identity. Include the GitHub URL, five-commit
log, every numbered answer A1--E, prediction/actual tables, diagrams, and
screenshots in an appendix. Do not claim account-dependent results until you
have run them yourself.

