import httpx
class FuyaoClient:
 def __init__(self,base_url,key): self.base=base_url.rstrip('/');self.key=key
 async def get(self,path,**params):
  if not self.key: raise RuntimeError('HITHINK_FINANCE_API_KEY 未配置')
  async with httpx.AsyncClient(timeout=30) as c:
   r=await c.get(self.base+path,params=params,headers={'X-api-key':self.key});r.raise_for_status();return r.json()
 async def snapshot(self,codes): return await self.get('/a-share/prices/snapshot',thscodes=','.join(codes))
