from localstack.utils.aws import aws_models
etAru=super
etArd=None
etArG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  etAru(LambdaLayer,self).__init__(arn)
  self.cwd=etArd
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.etArG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(RDSDatabase,self).__init__(etArG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(RDSCluster,self).__init__(etArG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(AppSyncAPI,self).__init__(etArG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(AmplifyApp,self).__init__(etArG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(ElastiCacheCluster,self).__init__(etArG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(TransferServer,self).__init__(etArG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(CloudFrontDistribution,self).__init__(etArG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,etArG,env=etArd):
  etAru(CodeCommitRepository,self).__init__(etArG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
