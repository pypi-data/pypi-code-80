import torch
from torch import nn
from collections import OrderedDict
class ExtractionLayer(nn.Module):

    def __init__(self,fn : callable = lambda x : x):
        super(self.__class__,self).__init__()
        self.fn = fn

    def forward(self,*args,**kwargs):return self.fn( *args, **kwargs )

def _conv_transpose(conv) -> nn.Module:
    """[summary]

    :param conv: [description]
    :type conv: [type]
    :return: [description]
    :rtype: nn.Module
    """        
    def _copy(cnv): 
        d = { (key ) :getattr(cnv,key) for key in 'in_channels,out_channels,kernel_size,stride,dialation,padding,groups,padding_mode'.split(',') if hasattr(cnv,key) }
        ic = d['in_channels']
        d['in_channels'] = d['out_channels']
        d['out_channels'] = ic
        return d
    conv_table = {
        'Conv1d':nn.ConvTranspose1d,
        'Conv2d':nn.ConvTranspose2d,
        'Conv3d':nn.ConvTranspose3d
    }
    # we want to check if the Conv layer is a build in class like "Conv2d" or a custom class with conv in it like "BasicConv2d"
    if conv.__class__.__name__ not in conv_table:
        return nn.Sequential(
            *(_check_transpose(child) for child in list(conv.children())[::-1] )
        )
    cnv = conv_table[conv.__class__.__name__]( **_copy( conv ) ) 
    cnv.weight.data = conv.weight.data #.permute(1,0,2) if len( conv.weight.data.size() ) == 3 else conv.weight.data.permute(1,0,2,3)
    return cnv

def _linear_transpose(linear) -> nn.Module:
    """[summary]

    :param linear: [description]
    :type linear: [type]
    :return: [description]
    :rtype: nn.Module
    """
    layer = nn.Linear(
        in_features=linear.out_features,
        out_features=linear.in_features,
    ) 
    layer.weight.data = linear.weight.data.t()
    return layer


def _pool_transpose( pooling : nn.Module ) -> nn.Module:
    """
    Right now we are only applying the MaxUnpool function for all pooling methods. TODO: comeback and figure out a way to do that for other methods
    :param pooling: [description]
    :type pooling: nn.Module
    :return: [description]
    :rtype: nn.Module
    """
    def _copy(pool): 
        # if hasattr(pool,'kernel_size'):
        return { ( key ) :getattr(pool,key) for key in 'kernel_size,stride,padding,dialation'.split(',') if hasattr(pool,key) }
        # else:
    pool_table = {
        'MaxPool1d':nn.MaxUnpool1d,
        'MaxPool2d':nn.MaxUnpool2d,
        'MaxPool3d':nn.MaxUnpool3d,

        'AvgPool1d':nn.MaxUnpool1d,
        'AvgPool2d':nn.MaxUnpool2d,
        'AvgPool3d':nn.MaxUnpool3d,

        'AdaptiveMaxPool1d':nn.MaxUnpool1d,
        'AdaptiveMaxPool2d':nn.MaxUnpool2d,
        'AdaptiveMaxPool3d':nn.MaxUnpool3d,

        # 'AdaptiveAvgPool1d':nn.MaxUnpool1d,
        # 'AdaptiveAvgPool2d':nn.MaxUnpool2d,
        # 'AdaptiveAvgPool3d':nn.MaxUnpool3d
    }
    # we want to check if the Conv layer is a build in class like "Conv2d" or a custom class with conv in it like "BasicConv2d"
    if pooling.__class__.__name__ not in pool_table:
        return nn.Sequential(
            *(_check_transpose(child) for child in list(pooling.children())[::-1] )
        )
    # print(pooling)
    # print( pool_table[pooling.__class__.__name__]( **_copy( pooling ) )  )
    # print( _copy( pooling ) )
    # print('-'*80)
    return pool_table[pooling.__class__.__name__]( **_copy( pooling ) ) 


def _copy_transpose(param):
    if 'Conv' in param.__class__.__name__:return _conv_transpose( param )
    elif 'Linear' in param.__class__.__name__: return _linear_transpose( param )
    elif 'Pool' in param.__class__.__name__: return _pool_transpose( param )
    # elif 'BatchNorm' in param.__class__.__name__: return param.eval()


    # it's an activation function, so just return it
    return param

def _check_transpose(param) -> nn.Module :
    """
    

    :param param: [description]
    :type param: [type]
    :return: [description]
    :rtype: nn.Module
    """    
    if 'Print' in param.__class__.__name__:return param    
    children = list( param.children() )[::-1]
    # print(len(children))
    module = nn.Sequential(
        *([_check_transpose( child ) for child in children ]+([ _copy_transpose( param ) ] if not len(children) > 0 else [] ))
    ) 
    return module

def _find_pooling_layers(module,table=OrderedDict(),names={
        'MaxPool1d',
        'MaxPool2d',
        'MaxPool3d',

        'AvgPool1d',
        'AvgPool2d',
        'AvgPool3d',

        'AdaptiveMaxPool1d',
        'AdaptiveMaxPool2d',
        'AdaptiveMaxPool3d'

        # 'AdaptiveAvgPool1d',
        # 'AdaptiveAvgPool2d',
        # 'AdaptiveAvgPool3d'
    },parent='',depth=0):
    children = list(module.named_children())[::-1]
    for i,(k,v) in enumerate(children):
        grand_kids = list(v.children())
        if len(grand_kids) > 0: 
            for j,gk in enumerate(grand_kids):table.update( _find_pooling_layers( gk,table,names,k,j) )
        if v.__class__.__name__ in names:
            # print('saving',k,i)
            table.update( {f'{k}{"."+str(i)}': v})
    if module.__class__.__name__ in names:
        # print('adding',parent,depth)
        table.update( {f"{parent}.{depth}":module} )
    return table

def _find_unpooling_layers(module,table=OrderedDict(),names={
        'MaxUnpool1d',
        'MaxUnpool2d',
        'MaxUnpool3d'
    },parent='',depth=0):
    children = list(module.named_children())[::-1]
    for i,(k,v) in enumerate(children):
        grand_kids = list(v.children())
        if len(grand_kids) > 0: 
            for j,gk in enumerate(grand_kids):table.update( _find_unpooling_layers( gk,table,names,k,j) )
        if v.__class__.__name__ in names:
            table.update( {f'{parent}{"."+str(depth)}{"."+str(i)}': v})

    if module.__class__.__name__ in names:
        table.update( {f"{parent}.{depth}":module} )
    return table

def _inject_new_layer(model,key,layer):
    keys = key.split('.')
    m = model
    # iterate through layers then replace the layer
    for k in keys[:-1]:m = m[int(k)] if k.isnumeric() else getattr(m,k) 
    m.add_module(keys[-1],layer)
    return model

def _resolve_output_size(table,key,model):
    mod,index = table[key]
    key = list(table.items())[index-2][0]
    keys = key.split('.')
    m = model
    for k in keys:m = m[int(k)] if k.isnumeric() else getattr(m,k) 
    return m.weight.size()

def _assign_output_size(model,key,output_size):
    keys = key.split('.')
    m = model
    for k in keys:m = m[int(k)] if k.isnumeric() else getattr(m,k) 
    m.output_size = output_size
    return model

def _create_pooling_maps( enc,dec ):
    pooling_layers = _find_pooling_layers( enc )
    
    unpooling_layers = _find_unpooling_layers( dec )

    
    assert len(pooling_layers) == len(unpooling_layers),\
           f'There was an error in locating the pooling/unpooling layers ( {len(pooling_layers)} Pooling Layers vs {len(unpooling_layers)} Unpooling Layers )'
    modules = OrderedDict({k:(v,i) for i,(k,v) in enumerate(m.named_modules())} )
    output_sizes = {}
    for (enc_name,enc_layer),(dec_name,dec_layer) in zip(list(pooling_layers.items())[::-1],unpooling_layers.items() ):
        ipl = InvertablePoolingLayer( enc_layer )
        pm = PoolingMap( ipl, dec_layer )

        output_sizes.update({dec_name: _resolve_output_size( modules,enc_name,enc ) })

        enc = _inject_new_layer( enc, enc_name, ipl )
        dec = _inject_new_layer( dec, dec_name, pm  )
    for k,v in unpooling_layers.items():_assign_output_size( dec, k, output_sizes[k] )




class InvertablePoolingLayer(nn.Module):
    def __init__(self,fn : nn.Module):
        super(self.__class__,self).__init__()
        if not hasattr(fn,'return_indices'):
            self.return_indices = False
            self.fn = lambda x: (fn(x),torch.randperm(x.size()).view(x.size()))
            
        else:
            self.return_indices = fn.return_indices
            fn.return_indices = True
            self.fn = fn
        
        self.indices = None
        self.y = None
        self.x = None
        

    def forward(self,x : torch.Tensor) -> torch.Tensor:
        self.x = x
        self.y,self.indices = self.fn(x)
        return ( self.y if not self.return_indices else (self.y,self.indices) )

class PoolingMap(nn.Module):

    def __init__(self,pooling_layer : InvertablePoolingLayer,unpooling_layer:nn.Module):
        super(self.__class__,self).__init__()
        self.pooling_layer = pooling_layer
        self.unpooling_layer = unpooling_layer
        self.output_size = None

    def unpool(self,x) -> torch.Tensor:
        
        return self.unpooling_layer( x, self.pooling_layer.indices )
    
    def forward(self,x) -> torch.Tensor:
        if len(x.size()) < 3:x = x.view(1,256,6,6)

        y = self.unpooling_layer( x , self.pooling_layer.indices,self.pooling_layer.x.size() )
        return y

class PassThrough(nn.Module):
    def forward(self,x):return x

class GenerativeAutoEncoder(nn.Module):   

    def __init__(self,model : nn.Module ,feature_layer : str = None, translation_layer : nn.Module = None):
        """[summary]

        :param model: [description]
        :type model: nn.Module
        :param feature_layer: [description], defaults to None
        :type feature_layer: str, optional
        """        
        super(self.__class__,self).__init__()
        self.enc = model
        self.dec = self._build_dec( self.enc )
        self.trans = translation_layer
        # print( self.enc );exit()
        _create_pooling_maps( self.enc, self.dec )
    

    def forward(self,*args,**kwargs): 
        _y =  self.enc( *args, **kwargs )
        if self.trans is not None:_y = self.trans( _y )
        return self.dec( _y )

    def _build_dec(self, model : nn.Module ) -> nn.Module :
        """
        Consume the encoder model and return the reversed model

        :param model: [description]
        :type model: nn.Module
        :return: [description]
        :rtype: nn.Module
        """     
        module_list = []
        for param in list(model.children())[::-1]:        
            module_list.append( _check_transpose(param) )
        return nn.Sequential(*module_list)
class Print(nn.Module):

    def forward(self,x):
        print(x.size())
        return x#.permute(0,2,1)
if __name__ == '__main__':
    import torchvision.models as models
    m = nn.Sequential(
        nn.Linear(100,200),
        nn.Sequential(
            nn.Linear(200,100),
            nn.ELU(),
            nn.Linear(100,200),
            # Print(),
            # ExtractionLayer( lambda output:output.permute(1,0,2) ),
            # nn.LSTM(200,200,3),
            # ExtractionLayer( lambda output:output[0] )
        ),
        nn.Sequential(
            nn.Linear(200,100),
            nn.ELU(),
            # nn.Linear(100,200),
            # nn.Conv1d(1,100,1),
            # Print(),
            nn.Linear(100,200)
        ),
        nn.ReLU(),
        nn.Linear(200,10)
    )
    m = models.alexnet()

    gae = GenerativeAutoEncoder(
                                m,
                                # translation_layer=ExtractionLayer( lambda x:x.unsqueeze(0) )
                                ).eval()
    x = torch.randn( (1,3,223,223) )
    y = torch.randn( (1,1000) )
    # x = torch.randn( (5,100) )
    with torch.no_grad():print(
        (gae(x) - x).mean()
    )
