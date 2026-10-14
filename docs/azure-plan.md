# Azure Deployment Plan

## Objective
The objective is to deploy the Azure Support Ticket Automation API to Microsoft Azure so it can be accessed online.

## Proposed Azure Services
- **Azure App Service:** Host the FastAPI backend.
- **Azure Container Registry (ACR):** Store the Docker image, if deploying the container image.
- **Microsoft Entra ID:** Provide identity for secure deployment authentication.
- **GitHub Actions:** Automate testing and deployment workflows.

## Deployment Steps
1. Run the application and automated tests locally.
2. Build the Docker image and verify that the API starts correctly.
3. Create an Azure resource group and the required hosting resources.
4. Configure GitHub Actions to authenticate with Azure using OpenID Connect (OIDC).
5. Build and publish the container image to Azure Container Registry, if using the container-based approach.
6. Deploy the image to the selected Azure hosting service.
7. Configure the required application settings and verify the deployed API health endpoint.

## Security Considerations
- Use GitHub repository secrets or environment configuration only for values that genuinely require secrets.
- Prefer OpenID Connect (OIDC) with Microsoft Entra ID over long-lived Azure credentials.
- Never commit passwords, access tokens, connection strings, or other secrets.
- Restrict deployment permissions to the required Azure resources.

## Current Status
The application has been tested locally and the Docker image builds successfully. Azure deployment is a planned next step and is not yet confirmed as completed.

## Verification
After deployment:
- Check the API health endpoint.
- Test ticket creation and retrieval.
- Test duplicate ID and invalid input handling.
- Verify the approval workflow.
- Review GitHub Actions logs for successful testing and deployment.
