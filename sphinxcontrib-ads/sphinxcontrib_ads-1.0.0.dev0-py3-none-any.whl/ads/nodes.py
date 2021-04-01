from docutils.nodes import General, Element


class AdsJavascriptNode(General, Element):
    """Add javascript node for inline Ads."""

    @staticmethod
    def visit(self, node):
        if node['ads']['vendor'] == 'carbonads':
            attrs = {
                'async': '',
                'ids': ['_carbonads_js'],  # it's "ids" and NOT "id" as per docutils docs
                'src': node['ads']['attributes']['url']
            }
        elif node['ads']['vendor'] == 'ethicalads':
            attrs = {
                'async': '',
                'src': 'https://media.ethicalads.io/media/client/ethicalads.min.js'
            }

        self.body.append(self.starttag(node, 'script', '', **attrs))

    @staticmethod
    def depart(self, node):
        self.body.append('</script>')

class AdsPlacementNode(General, Element):
    """Add placement node for inline Ads."""

    @staticmethod
    def visit(self, node):
        if node['ads']['vendor'] == 'ethicalads':

            attrs = {}

            # "data-ea-publisher" is the only required attribute
            attrs['data-ea-publisher'] = node['ads']['attributes']['data-ea-publisher']

            # optional attributes
            if node['ads']['attributes']['data-ea-type']: attrs['data-ea-type'] = node['ads']['attributes']['data-ea-type']
            if node['ads']['attributes']['data-ea-keywords']: attrs['data-ea-keywords'] = node['ads']['attributes']['data-ea-keywords']
            if node['ads']['attributes']['data-ea-campaign-types']: attrs['data-ea-campaign-types'] = node['ads']['attributes']['data-ea-campaign-types']
            if node['ads']['attributes']['data-ea-manual']: attrs['data-ea-manual'] = node['ads']['attributes']['data-ea-manual']
            if node['ads']['attributes']['class']: attrs['class'] = node['ads']['attributes']['class']
            if node['ads']['attributes']['id']: attrs['id'] = node['ads']['attributes']['id']

        self.body.append(self.starttag(node, 'div', '', **attrs))

    @staticmethod
    def depart(self, node):
        self.body.append('</div>')
