def ServiceAccountModelJson (namespace: str,serviceAccount: str):
    """_summary_

    Args:
        namespace (str): Namespace name
        serviceAccount (str): Service Account name

    Returns:
        _type_: _description_
    """
    return {
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "name": serviceAccount,
        "namespace": namespace,
    }
}