MAColTypes = {}
MAColTypes['mag'] = {}

MAColTypes['mag']['long'] = ['EstimatedCitation',
                             'JournalId',
                             'FieldOfStudyId2',
                             'AffiliationId',
                             'RecommendedPaperId',
                             'ConferenceInstanceId',
                             'ChildFieldOfStudyId',
                             'PaperFamilyCount',
                             'AuthorId',
                             'PaperCount',
                             'FamilyId',
                             'PaperId',
                             'EntityId',
                             'PaperReferenceId',
                             'FieldOfStudyId',
                             'ReferenceCount',
                             'ConferenceSeriesId',
                             'RelatedEntityId',
                             'FieldOfStudyId1',
                             'LastKnownAffiliationId',
                             'CitationCount']

MAColTypes['mag']['int'] = ['AuthorSequenceNumber',
                            'Rank',
                            'RelationshipType',
                            'Year',
                            'ResourceType',
                            'FamilyRank',
                            'AttributeType',
                            'RelatedType',
                            'SourceType']

MAColTypes['mag']['float'] = ['Latitude',
                              'Longitude',
                              'Score',
                              'Rank']

MAColTypes['nlp'] = {}
MAColTypes['nlp']['long'] = ['PaperId', 'PaperReferenceId']

MAColTypes['advanced'] = {}
MAColTypes['advanced']['long'] = [
    'EntityId',
    'RelatedEntityId',
    'FieldOfStudyId',
    'ChildFieldOfStudyId',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'PaperId',
    'RecommendedPaperId',
    'FieldOfStudyId1',
    'FieldOfStudyId2']
MAColTypes['advanced']['int'] = [
    'RelatedType',
    'AttributeType',
    'Rank',
    'Level']
MAColTypes['advanced']['float'] = ['Score']

MAColumnNames = {}
MAColumnNames['mag'] = {}
MAColumnNames['mag']['Authors'] = [
    'AuthorId',
    'Rank',
    'NormalizedName',
    'DisplayName',
    'LastKnownAffiliationId',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'CreatedDate']
MAColumnNames['mag']['Authors_indexes'] = [
    ('AuthorId', 1), ('LastKnownAffiliationId', 1)]

MAColumnNames['mag']['Affiliations'] = [
    'AffiliationId',
    'Rank',
    'NormalizedName',
    'DisplayName',
    'GridId',
    'OfficialPage',
    'WikiPage',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'Latitude',
    'Longitude',
    'CreatedDate']
MAColumnNames['mag']['Affiliations_indexes'] = [
    ('AffiliationId', 1), ('GridId', 1)]

MAColumnNames['mag']['PaperAuthorAffiliations'] = [
    'PaperId',
    'AuthorId',
    'AffiliationId',
    'AuthorSequenceNumber',
    'OriginalAuthor',
    'OriginalAffiliation']
MAColumnNames['mag']['PaperAuthorAffiliations_indexes'] = [
    ('PaperId', 1), ('AuthorId', 1), ('AffiliationId', 1)]

MAColumnNames['mag']['Papers'] = [
    'PaperId',
    'Rank',
    'Doi',
    'DocType',
    'PaperTitle',
    'OriginalTitle',
    'BookTitle',
    'Year',
    'Date',
    'Publisher',
    'JournalId',
    'ConferenceSeriesId',
    'ConferenceInstanceId',
    'Volume',
    'Issue',
    'FirstPage',
    'LastPage',
    'ReferenceCount',
    'CitationCount',
    'EstimatedCitation',
    'OriginalVenue',
    'FamilyId',
    'CreatedDate']
MAColumnNames['mag']['Papers_indexes'] = [
    ('PaperId',
     1),
    ('JournalId',
     1),
    ('ConferenceSeriesId',
     1),
    ('ConferenceInstanceId',
     1),
    ('FamilyId',
     1),
    ("Doi",
     "text")]

MAColumnNames['mag']['PaperUrls'] = [
    'PaperId',
    'SourceType',
    'SourceUrl',
    'LanguageCode']
MAColumnNames['mag']['PaperUrls_indexes'] = [('PaperId', 1)]

MAColumnNames['mag']['PaperResources'] = [
    'PaperId',
    'ResourceType',
    'ResourceUrl',
    'SourceUrl',
    'RelationshipType']
MAColumnNames['mag']['PaperResources_indexes'] = [('PaperId', 1)]

MAColumnNames['mag']['PaperReferences'] = ['PaperId', 'PaperReferenceId']
MAColumnNames['mag']['PaperReferences_indexes'] = [
    ('PaperId', 1), ('PaperReferenceId', 1)]

MAColumnNames['mag']['PaperExtendedAttributes'] = [
    'PaperId', 'AttributeType', 'AttributeValue']
MAColumnNames['mag']['PaperExtendedAttributes_indexes'] = [('PaperId', 1)]

MAColumnNames['mag']['Journals'] = [
    'JournalId',
    'Rank',
    'NormalizedName',
    'DisplayName',
    'Issn',
    'Publisher',
    'Webpage',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'CreatedDate']
MAColumnNames['mag']['Journals_indexes'] = [('JournalId', 1)]

MAColumnNames['mag']['ConferenceSeries'] = [
    'ConferenceSeriesId',
    'Rank',
    'NormalizedName',
    'DisplayName',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'CreatedDate']
MAColumnNames['mag']['ConferenceSeries_indexes'] = [('ConferenceSeriesId', 1)]

MAColumnNames['mag']['ConferenceInstances'] = [
    'ConferenceInstanceId',
    'NormalizedName',
    'DisplayName',
    'ConferenceSeriesId',
    'Location',
    'OfficialUrl',
    'StartDate',
    'EndDate',
    'AbstractRegistrationDate',
    'SubmissionDeadlineDate',
    'NotificationDueDate',
    'FinalVersionDueDate',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'Latitude',
    'Longitude',
    'CreatedDate']
MAColumnNames['mag']['ConferenceInstances_indexes'] = [
    ('ConferenceInstanceId', 1), ('ConferenceSeriesId', 1)]


MAColumnNames['nlp'] = {}
MAColumnNames['nlp']['PaperAbstractsInvertedIndex'] = [
    'PaperId', 'IndexedAbstract']
MAColumnNames['nlp']['PaperAbstractsInvertedIndex_indexes'] = [('PaperId', 1)]
MAColumnNames['nlp']['PaperCitationContexts'] = [
    'PaperId', 'PaperReferenceId', 'CitationContext']
MAColumnNames['nlp']['PaperCitationContexts_indexes'] = [
    ('PaperId', 1), ('PaperReferenceId', 1)]

MAColumnNames['advanced'] = {}
MAColumnNames['advanced']['EntityRelatedEntities'] = [
    'EntityId',
    'EntityType',
    'RelatedEntityId',
    'RelatedEntityType',
    'RelatedType',
    'Score']
MAColumnNames['advanced']['EntityRelatedEntities_indexes'] = [
    ('EntityId', 1), ('RelatedEntityId', 1)]
MAColumnNames['advanced']['FieldOfStudyChildren'] = [
    'FieldOfStudyId', 'ChildFieldOfStudyId']
MAColumnNames['advanced']['FieldOfStudyChildren_indexes'] = [
    ('FieldOfStudyId', 1), ('ChildFieldOfStudyId', 1)]
MAColumnNames['advanced']['FieldOfStudyExtendedAttributes'] = [
    'FieldOfStudyId', 'AttributeType', 'AttributeValue']
MAColumnNames['advanced']['FieldOfStudyExtendedAttributes_indexes'] = [
    ('FieldOfStudyId', 1)]
MAColumnNames['advanced']['FieldsOfStudy'] = [
    'FieldOfStudyId',
    'Rank',
    'NormalizedName',
    'DisplayName',
    'MainType',
    'Level',
    'PaperCount',
    'PaperFamilyCount',
    'CitationCount',
    'CreatedDate']
MAColumnNames['advanced']['FieldsOfStudy_indexes'] = [('FieldOfStudyId', 1)]
MAColumnNames['advanced']['PaperFieldsOfStudy'] = [
    'PaperId', 'FieldOfStudyId', 'Score']
MAColumnNames['advanced']['PaperFieldsOfStudy_indexes'] = [
    ('PaperId', 1), ('FieldOfStudyId', 1)]
MAColumnNames['advanced']['PaperRecommendations'] = [
    'PaperId', 'RecommendedPaperId', 'Score']
MAColumnNames['advanced']['PaperRecommendations_indexes'] = [
    ('PaperId', 1), ('RecommendedPaperId', 1)]
MAColumnNames['advanced']['RelatedFieldOfStudy'] = [
    'FieldOfStudyId1', 'Type1', 'FieldOfStudyId2', 'Type2', 'Rank']
MAColumnNames['advanced']['RelatedFieldOfStudy_indexes'] = [
    ('FieldOfStudyId1', 1), ('FieldOfStudyId2', 1)]

MACollectionNames = {}
MACollectionNames['mag'] = [
    'Authors',
    'Affiliations',
    'PaperAuthorAffiliations',
    'Papers',
    'PaperUrls',
    'PaperResources',
    'PaperReferences',
    'PaperExtendedAttributes',
    'Journals',
    'ConferenceSeries',
    'ConferenceInstances']
MACollectionNames['nlp'] = [
    'PaperAbstractsInvertedIndex',
    'PaperCitationContexts']
MACollectionNames['advanced'] = [
    'EntityRelatedEntities',
    'FieldOfStudyChildren',
    'FieldOfStudyExtendedAttributes',
    'FieldsOfStudy',
    'PaperFieldsOfStudy',
    'PaperRecommendations',
    'RelatedFieldOfStudy']
