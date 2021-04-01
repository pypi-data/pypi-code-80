from localstack.utils.aws import aws_models
UksPz=super
UksPJ=None
UksPx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UksPz(LambdaLayer,self).__init__(arn)
  self.cwd=UksPJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.UksPx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(RDSDatabase,self).__init__(UksPx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(RDSCluster,self).__init__(UksPx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(AppSyncAPI,self).__init__(UksPx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(AmplifyApp,self).__init__(UksPx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(ElastiCacheCluster,self).__init__(UksPx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(TransferServer,self).__init__(UksPx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(CloudFrontDistribution,self).__init__(UksPx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,UksPx,env=UksPJ):
  UksPz(CodeCommitRepository,self).__init__(UksPx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
