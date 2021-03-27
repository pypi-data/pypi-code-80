from localstack.utils.aws import aws_models
AKVvm=super
AKVvg=None
AKVvl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AKVvm(LambdaLayer,self).__init__(arn)
  self.cwd=AKVvg
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AKVvl.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(RDSDatabase,self).__init__(AKVvl,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(RDSCluster,self).__init__(AKVvl,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(AppSyncAPI,self).__init__(AKVvl,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(AmplifyApp,self).__init__(AKVvl,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(ElastiCacheCluster,self).__init__(AKVvl,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(TransferServer,self).__init__(AKVvl,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(CloudFrontDistribution,self).__init__(AKVvl,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AKVvl,env=AKVvg):
  AKVvm(CodeCommitRepository,self).__init__(AKVvl,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
