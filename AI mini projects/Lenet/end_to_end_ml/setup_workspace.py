import os, json, sys, argparse
import azureml.core
from azureml.core import Workspace
from azureml.exceptions import WorkspaceException
from azureml.core.authentication import AzureCliAuthentication
import mlflow
import mlflow.azureml


def main(workspace_name=None, subscription_id=None, resource_group=None):
    try:
        workspace = Workspace.get(name=workspace_name,
                                  subscription_id=subscription_id,
                                  resource_group=resource_group)
        print(f'''Workspace name: {workspace.name}\nWorkspace region: {workspace.location}\nWorkspace subscription ID: {workspace.subscription_id[:3]}---xxxx---{workspace.subscription_id[-3:]}\nWorkspace resource group: {workspace.resource_group}''')
        workspace.write_config(
            path=os.getenv("WORKSPACE_CONFIG_PATH", "./"),
            file_name=os.getenv("WORKSPACE_CONFIG_NAME", "workspace_congif.json")
        )
        print("Successfully loaded Workspace")
    except Exception as e:
        raise e


if __name__ == '__main__':
    # fetching arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace_name', type=str, default=os.getenv("WORKSPACE_NAME", None), help='Workspace name')
    parser.add_argument('--subscription_id', type=str, default=os.getenv("SUBSCRIPTION_ID", None), help='Subscription ID')
    parser.add_argument('--resource_group', type=str, default=os.getenv("RESOURCE_GROUP", None), help='Resource group')
    args = parser.parse_args()

    # running model
    main(workspace_name=args.workspace_name,
         subscription_id=args.subscription_id,
         resource_group=args.resource_group)