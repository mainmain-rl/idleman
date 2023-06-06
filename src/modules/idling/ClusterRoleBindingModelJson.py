def ClusterRoleBindingModelJson (
    namespace: str,
    clusterRoleBindingName: str,
    serviceAccount: str
    ):
    """Get json to create clusterRoleBinding 
        directly connected to the ClusterRole "cr-idling".

    Args:
        namespace (str): Namespace name.
        clusterRoleBindingName (str): ClusterRoleBinding name.
        serviceAccount (str): Service Account Name to bind it.

    Returns:
        dict: json body.
    """
    return {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {
            "name": clusterRoleBindingName,
            "namespace": namespace
        },
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "cr-idling"
        },
        "subjects": [
            {
                "kind": "ServiceAccount",
                "name": serviceAccount,
                "namespace": namespace
            }
        ]
    }