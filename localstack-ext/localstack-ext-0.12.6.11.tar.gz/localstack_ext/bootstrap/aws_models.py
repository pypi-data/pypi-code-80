from localstack.utils.aws import aws_models
iluTj=super
iluTw=None
iluTd=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iluTj(LambdaLayer,self).__init__(arn)
  self.cwd=iluTw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.iluTd.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(RDSDatabase,self).__init__(iluTd,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(RDSCluster,self).__init__(iluTd,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(AppSyncAPI,self).__init__(iluTd,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(AmplifyApp,self).__init__(iluTd,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(ElastiCacheCluster,self).__init__(iluTd,env=env)
class TransferServer(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(TransferServer,self).__init__(iluTd,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(CloudFrontDistribution,self).__init__(iluTd,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,iluTd,env=iluTw):
  iluTj(CodeCommitRepository,self).__init__(iluTd,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
