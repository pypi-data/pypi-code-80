from localstack.utils.aws import aws_models
cqjyS=super
cqjyb=None
cqjyx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cqjyS(LambdaLayer,self).__init__(arn)
  self.cwd=cqjyb
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cqjyx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(RDSDatabase,self).__init__(cqjyx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(RDSCluster,self).__init__(cqjyx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(AppSyncAPI,self).__init__(cqjyx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(AmplifyApp,self).__init__(cqjyx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(ElastiCacheCluster,self).__init__(cqjyx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(TransferServer,self).__init__(cqjyx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(CloudFrontDistribution,self).__init__(cqjyx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cqjyx,env=cqjyb):
  cqjyS(CodeCommitRepository,self).__init__(cqjyx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
