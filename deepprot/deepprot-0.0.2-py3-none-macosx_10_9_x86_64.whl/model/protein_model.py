import deepprot as dp

antibodies = dp.data.Dataset("../../../../test_data/secondary_structure_cb513.pkl")
dl = dp.data.DataLoader(antibodies, featurizer=dp.feat.KideraFactors())
model = dp.model.CNN()
model.fit(dl)
