from localstack.utils.aws import aws_models
XsVqw=super
XsVqf=None
XsVqg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XsVqw(LambdaLayer,self).__init__(arn)
  self.cwd=XsVqf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XsVqg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(RDSDatabase,self).__init__(XsVqg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(RDSCluster,self).__init__(XsVqg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(AppSyncAPI,self).__init__(XsVqg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(AmplifyApp,self).__init__(XsVqg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(ElastiCacheCluster,self).__init__(XsVqg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(TransferServer,self).__init__(XsVqg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(CloudFrontDistribution,self).__init__(XsVqg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XsVqg,env=XsVqf):
  XsVqw(CodeCommitRepository,self).__init__(XsVqg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
