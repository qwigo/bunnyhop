import unittest
from envs import env
from bunnyhop import Bunny

class Test_GettingStarted(unittest.TestCase):
    def setUp(self):
        b = Bunny(env('BUNNYCDN_API_KEY'))
        self.b = b

    def tearDown(self):
        self.b = None

    def test_ListPullZone(self):
        # Arrange
        from bunnyhop.zone import Zone

        # Act
        l = self.b.Zone.list()

        # Assert
        self.assertIsInstance(l,list)
        self.assertIsInstance(l[0], Zone)

    def test_GetAPullZone(self):
        # Arrange
        from bunnyhop.zone import Zone
        goodwebsiteAId = 164657

        # Act
        zone = self.b.Zone.get(id=goodwebsiteAId)
        
        # Assert
        self.assertIsInstance(zone, Zone)
        self.assertEqual(zone.Id, goodwebsiteAId)

    def test_CreateAPullZone(self):
        # Arrange
        name = 'testZone'
        testType = 0
        originUrl = 'https://testZone.org'
        storageZoneId = 'testStorageZoneId' 

        # Act
        self.b.Zone.create(
                Name=name,
                Type=testType, # 0 = Standard and 1 = High Volume
                OriginUrl=originUrl,
                StorageZoneId=storageZoneId)
        testList = self.b.Zone.list()
        testId = testList[-1].Id
        print(testList)
        print(testId)
        
        # Assert
        testzone = self.b.Zone.get(id=testId)
        self.assertEqual(testzone.Name, name)
        self.assertEqual(testzone.Type, testType)
        self.assertEqual(testzone.OriginUrl, originUrl)
        self.assertEqual(testzone.StorageZoneId, storageZoneId)
        testzone.delete()

if __name__ == "__main__":
    unittest.main()
