# deploy_to_gcloud.ps1
# Automates deployment of the CyberQuant website to Google Cloud App Engine

$ProjectID = "tribal-terra-446412-n4"

Write-Host "🚀 Starting deployment for Project: $ProjectID" -ForegroundColor Cyan

# Build Tailwind CSS for production
Write-Host "Building Tailwind CSS..."
npm run build:css
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tailwind CSS build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Tailwind CSS built successfully." -ForegroundColor Green

# Ensure the correct project is selected
Write-Host "Setting Google Cloud Project..."
gcloud config set project $ProjectID

# Deploy to App Engine
# --quiet: disable interactive prompts
# --promote: send all traffic to the new version (default behavior)
# --stop-previous-version: stop previous version to save costs (optional, good for static sites)
Write-Host "uploading files and deploying... (this may take a minute)"
gcloud app deploy app.yaml --project=$ProjectID --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment Successful!" -ForegroundColor Green
    Write-Host "🌍 Your site is live at: https://$ProjectID.uc.r.appspot.com" -ForegroundColor Cyan
} else {
    Write-Host "❌ Deployment Failed!" -ForegroundColor Red
}
