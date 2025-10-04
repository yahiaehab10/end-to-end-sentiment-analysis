# Quick Setup Guide

## 1. Add GitHub Secrets

To enable model registration to DagsHub/MLflow, add these secrets:

### Steps:

1. Go to: `https://github.com/yahiaehab10/end-to-end-sentiment-analysis/settings/secrets/actions`
2. Click **"New repository secret"**
3. Add each secret:

| Secret Name        | Description           | Where to get it                    |
| ------------------ | --------------------- | ---------------------------------- |
| `DAGSHUB_USERNAME` | Your DagsHub username | Your DagsHub profile               |
| `DAGSHUB_TOKEN`    | DagsHub access token  | DagsHub → Settings → Access Tokens |

### Get DagsHub Token:

1. Login to DagsHub: https://dagshub.com/
2. Go to: **User Settings** → **Access Tokens**
3. Click **"Create Token"**
4. Copy and save the token (you won't see it again!)
5. Add it to GitHub secrets as `DAGSHUB_TOKEN`

## 2. Verify Workflows

After adding secrets, test the workflows:

```bash
# Commit and push your changes
git add .
git commit -m "fix: Update workflows and dependencies"
git push origin main
```

Then check: `https://github.com/yahiaehab10/end-to-end-sentiment-analysis/actions`

## 3. Expected Workflow Results

### ✅ Should Pass:

- Lint and test job
- Security scan
- Docker build (on PR)

### ⚠️ May Skip:

- Data validation (if data files not in repo)
- Model training (only runs on push to main)

### ❌ Expected Failures (until secrets added):

- Model registration (needs DAGSHUB secrets)

## 4. Monitor Workflow Runs

View all workflow runs:

```
https://github.com/yahiaehab10/end-to-end-sentiment-analysis/actions
```

Click on any run to see:

- ✅ Green checkmark = passed
- 🟡 Yellow dot = in progress
- ❌ Red X = failed
- ⚪ Gray circle = skipped

## 5. Download Artifacts

After successful model training:

1. Go to workflow run page
2. Scroll to **Artifacts** section
3. Download:
   - `model-artifacts` (trained models)
   - `security-report` (security scan results)

## 6. Troubleshooting

### Workflow not running?

- Check if `.github/workflows/` files are in main branch
- Verify YAML syntax is correct
- Check repository permissions allow Actions

### Model training fails?

- Verify data files exist in `data/raw/`
- Check Python version compatibility (should be 3.10)
- Review requirements.txt for correct package versions

### Docker build fails?

- Check Dockerfile syntax
- Verify model files exist (lgbm_model.pkl, tfidf_vectorizer.pkl)
- Review build logs for specific errors

### Secrets not working?

- Verify secret names match exactly (case-sensitive)
- Re-create the secret if needed
- Check DagsHub token hasn't expired

## Quick Commands

```bash
# View workflow status
gh workflow list

# Run workflow manually
gh workflow run "ML Pipeline CI/CD"

# View recent runs
gh run list

# View logs for latest run
gh run view --log
```

_Note: Requires GitHub CLI (`gh`) to be installed_
