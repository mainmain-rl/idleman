def CronJobModelJson(
        namespace: str, 
        deploymentName: str, 
        cronjobName: str,
        action: str, 
        image: str,
        schedule: str,
        service_account: str,
        replicas: str = "1"
        ):
        """Create a json body for idling cronjob.

        Args:
            namespace (str): Namespace name.
            deploymentName (str): Deployment name.
            cronjobName (str): Cronjob name.
            action (str): Action: pause or resume.
            image (str): Idling image.
            schedule (str): Schedule for cronjob action.
            service_account (str): Service Account to use for have an access to Kubernetes Cluster
            replicas (str): Number of replicas for the START action. Default to 1.

        Returns:
            dict: cronjob body json.
        """
        return {
            "apiVersion": "batch/v1",
            "kind": "CronJob",
            "metadata": {
                "name": cronjobName,
                "namespace": namespace,
            },
            "spec": {
                "failedJobsHistoryLimit": 14,
                "jobTemplate": {
                    "spec": {
                        "template": {
                            "spec": {
                                "containers": [
                                    {
                                        "env": [
                                            {
                                                "name": "ACTION",
                                                "value": action
                                            },
                                            {
                                                "name": "NAMESPACE",
                                                "value": namespace
                                            },
                                            {
                                                "name": "DEPLOYMENT",
                                                "value": deploymentName
                                            },
                                            {
                                                "name": "REPLICAS",
                                                "value": f"{replicas}"
                                            }
                                        ],
                                        "image": image,
                                        "imagePullPolicy": "IfNotPresent",
                                        "name": cronjobName,
                                        "resources": {
                                            "limits": {
                                                "cpu": "100m",
                                                "memory": "150Mi"
                                            },
                                            "requests": {
                                                "cpu": "50m",
                                                "memory": "100Mi"
                                            }
                                        },
                                    }
                                ],
                                "dnsPolicy": "ClusterFirst",
                                "restartPolicy": "OnFailure",
                                "serviceAccountName": service_account,
                            }
                        }
                    }
                },
                "schedule": schedule,
                "successfulJobsHistoryLimit": 14,
            },
        }