from localstack.utils.aws import aws_models
jOkDf=super
jOkDq=None
jOkDS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jOkDf(LambdaLayer,self).__init__(arn)
  self.cwd=jOkDq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.jOkDS.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(RDSDatabase,self).__init__(jOkDS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(RDSCluster,self).__init__(jOkDS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(AppSyncAPI,self).__init__(jOkDS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(AmplifyApp,self).__init__(jOkDS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(ElastiCacheCluster,self).__init__(jOkDS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(TransferServer,self).__init__(jOkDS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(CloudFrontDistribution,self).__init__(jOkDS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,jOkDS,env=jOkDq):
  jOkDf(CodeCommitRepository,self).__init__(jOkDS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
