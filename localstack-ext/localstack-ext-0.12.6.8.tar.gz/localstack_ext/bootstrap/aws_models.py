from localstack.utils.aws import aws_models
Rlncj=super
Rlnco=None
Rlncu=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Rlncj(LambdaLayer,self).__init__(arn)
  self.cwd=Rlnco
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Rlncu.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(RDSDatabase,self).__init__(Rlncu,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(RDSCluster,self).__init__(Rlncu,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(AppSyncAPI,self).__init__(Rlncu,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(AmplifyApp,self).__init__(Rlncu,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(ElastiCacheCluster,self).__init__(Rlncu,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(TransferServer,self).__init__(Rlncu,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(CloudFrontDistribution,self).__init__(Rlncu,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Rlncu,env=Rlnco):
  Rlncj(CodeCommitRepository,self).__init__(Rlncu,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
