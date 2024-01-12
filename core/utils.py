from utils.rpcs import rpc_list, chain_id_list
from utils.logger import logger


def get_rpc_provider(provider):
    provider = rpc_list.get(provider, None)
    if provider is not None:
        return provider
    logger.error("Incorrect RPC provider")


def get_rpc_chain(provider):
    chain_id = chain_id_list.get(provider, None)
    if chain_id is not None:
        return chain_id
    logger.error("Incorrect RPC chain id")
