from localstack.utils.aws import aws_models
bAgfV=super
bAgfx=None
bAgfq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bAgfV(LambdaLayer,self).__init__(arn)
  self.cwd=bAgfx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bAgfq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(RDSDatabase,self).__init__(bAgfq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(RDSCluster,self).__init__(bAgfq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(AppSyncAPI,self).__init__(bAgfq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(AmplifyApp,self).__init__(bAgfq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(ElastiCacheCluster,self).__init__(bAgfq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(TransferServer,self).__init__(bAgfq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(CloudFrontDistribution,self).__init__(bAgfq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bAgfq,env=bAgfx):
  bAgfV(CodeCommitRepository,self).__init__(bAgfq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
