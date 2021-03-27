from localstack.utils.aws import aws_models
Ymcwn=super
Ymcwp=None
Ymcwg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Ymcwn(LambdaLayer,self).__init__(arn)
  self.cwd=Ymcwp
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Ymcwg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(RDSDatabase,self).__init__(Ymcwg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(RDSCluster,self).__init__(Ymcwg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(AppSyncAPI,self).__init__(Ymcwg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(AmplifyApp,self).__init__(Ymcwg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(ElastiCacheCluster,self).__init__(Ymcwg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(TransferServer,self).__init__(Ymcwg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(CloudFrontDistribution,self).__init__(Ymcwg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Ymcwg,env=Ymcwp):
  Ymcwn(CodeCommitRepository,self).__init__(Ymcwg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
