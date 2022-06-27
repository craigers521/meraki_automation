import meraki

test = meraki.DashboardAPI('5b5a6a9b36bdab3c208d0fc152fce6c76367c243')
blah = test.batch.networks.updateNetwork('asdf1234', tags='somestuff')
print()
print(blah)