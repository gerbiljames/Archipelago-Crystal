from . import TeviTestBase

class TestLocationCheck(TeviTestBase):
    def test_Linebomb(self) -> None:
        location = ["North Thanatara Canyon - Blueberry Bunny Potion"]
        items = [["Cross Bomb"],["Cluster Bomb"]]
        self.assertAccessDependency(location,items,only_check_listed=True)

    def test_LibraryAcess(self) -> None:
        location = "Ana Thema - Sable"
        items = [self.get_item_by_name("Cross Bomb"),self.get_item_by_name("Library Key")]
        self.collect(items)
        self.assertTrue(self.can_reach_location(location))

    def test_Hands(self) -> None:
        location = "Forest Maze extended - Gilded Exultation"
        items = [self.get_item_by_name("Gilded Left Hand"),self.get_item_by_name("Gilded Right Hand"),self.get_item_by_name("Cross Bomb"),self.get_item_by_name("Double Rabi Boots")]
        self.collect(items)
        self.assertTrue(self.can_reach_location(location))

    def test_locations(self) -> None:
        items = self.collect_all_but([""])
        self.assertTrue(["Ulskan Village Area - Grape Bunny Potion"])





class TestMemine(TeviTestBase):
    run_default_tests = None
    options = {
        "open_morose": "1",
    }
    
    def test_Memine_Ticket(self) -> None:
        items =[self.get_item_by_name("Tartarus VIP Pass"),self.get_item_by_name("Valhalla VIP Pass")]
        
        locations = "Valhalla City - Memine Race From Tartarus"
        self.collect(items)
        self.assertFalse(self.can_reach_location(locations))
        self.assertTrue(self.can_reach_region("Tartarus"))

    def test_Forest_to_Copperwood(self) -> None:
        locations = ["CopperWood - Memine Race from Forest"]
        items = []
        self.collect(items)
        self.assertFalse(self.can_reach_location("CopperWood - Memine Race from Forest"))


class TestGalleryOfSouls(TeviTestBase):
    run_default_tests = None
    options = {
        "traverse_Mode": "random_teleporter",
    }
    
    def test_gallery_of_souls(self) -> None:
        items =[self.get_item_by_name("Cluster Bomb"),self.get_item_by_name("Slick Boots"),self.get_item_by_name("Double Rabi Boots"),self.get_item_by_name("Teleporter Gallery of Souls")]
        
        locations = "Gallery of Souls - Double Rabi Boots"
        self.collect(items)
        self.assertFalse(self.can_reach_location(locations))

