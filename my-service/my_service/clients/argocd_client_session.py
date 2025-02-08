# import aiohttp
# from cachetools import TTLCache
# from typing import Dict
# from my_service.models.models import ArgoCDCreds
# from my_service.utils.logger import setup_logger
# from my_service.config.config import settings
# import jwt
# import asyncio
# logger = setup_logger()


# class ArgoCDClientSessoin:
#     def __init__(self):
#         self.base_url = f"https://{settings.ARGOCD_URL}"
#         self.argocd_creds: ArgoCDCreds = ArgoCDCreds(
#             username=settings.ARGOCD_USERNAME,
#             password=settings.ARGOCD_PASSWORD
#         )
#         self.token_cache = TTLCache(maxsize=1, ttl=settings.TOKEN_CACHE_TTL)
#         self.session: aiohttp.ClientSession = aiohttp.ClientSession(
#             base_url=self.base_url
#         )

#     @classmethod
#     async def set_session_cookie(self):
#         token = await self._fetch_argocd_token()
#         logger.info(f"token >>>>>: {token}")
#         cookies = {
#             "argocd.token": token
#         }
#         self.session.cookie_jar.update_cookies(cookies)

#     async def _fetch_argocd_token(self):
#         """Fetch JWT token from ArgoCD and store it with TTL based on expiration."""

#         async with self.session as temp_session:
#             async with temp_session.post(
#                 f"https://{settings.ARGOCD_URL}/api/v1/session",
#                     json=self.argocd_creds.model_dump(),
#                     verify_ssl=False,
#             ) as resp:
#                 data = await resp.json()
#                 token = data.get("token")
#                 if token:
#                     logger.debug(
#                         f"ArgoCD session token has been successfully, setting up cache TTL")
#                     try:
#                         decoded = jwt.decode(
#                             token, options={"verify_signature": False})
#                         exp = decoded.get("exp", int(
#                             time.time()) + settings.TOKEN_CACHE_TTL)
#                         ttl = max(exp - int(time.time()) - 10, 60)
#                     except Exception:
#                         ttl = settings.TOKEN_CACHE_TTL
#                     self.token_cache.clear()
#                     self.token_cache[token] = ttl
#                     logger.info(f"***** token ***** :{token}")
#                     return token
#                 raise Exception("Failed to fetch ArgoCD token")

#     async def get_token(self):
#         """Retrieve token from cache or fetch a new one if expired."""
#         if not self.token_cache:
#             logger.info("Cache is empty, fetching a new token")
#             return await self._fetch_argocd_token()
#         logger.info("Cache hit! found token in cache")
#         logger.info(f"Cache: {self.token_cache}")
#         return next(iter(self.token_cache.keys()))

#     # def set_session_cookie(self, cookies: Dict):
#     #     self.session.cookie_jar.update_cookies = cookies


# # async def _init_argocd_client() -> ArgoCDClientSessoin:
# #     client =
# #     return client

# # argocd_client = ArgoCDClientSessoin()
