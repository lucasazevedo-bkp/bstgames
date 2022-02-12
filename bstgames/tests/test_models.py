from django.test import TestCase
from django.contrib.auth import get_user_model

from bstgames.models import (
    image_upload_path, GameGenre, GamePlatform, GameDeveloper, GamePublisher, 
    GamePlatformImage, GameGamePlatform, GameGameGenre, Game, GameMarket
)


class ImageUploadPathTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create()
        game_platform = GamePlatform.objects.create()
        game_game_platform = GameGamePlatform.objects.create(
            game=game, gameplatform=game_platform
        )
        self.game_platform_image = GamePlatformImage(
            gamegameplatform=game_game_platform
        )

    def test_image_upload_path(self):
        path = image_upload_path(self.game_platform_image, 'filename')
        gameplatform_id = self.game_platform_image.gamegameplatform.id
        path_compare = f'games/platforms/{gameplatform_id}_filename'
        self.assertEqual(path, path_compare)


class GameGenreTestCase(TestCase):

    def setUp(self):
        self.game_genre = GameGenre.objects.create(genre='genre')

    def test_str(self):
        self.assertEqual(self.game_genre.__str__(), self.game_genre.genre)


class GamePlatformTestCase(TestCase):

    def setUp(self):
        self.game_platform = GamePlatform.objects.create(platform='platform')

    def test_str(self):
        self.assertEqual(self.game_platform.__str__(), self.game_platform.platform)


class GameDeveloperTestCase(TestCase):

    def setUp(self):
        self.game_developer = GameDeveloper.objects.create(developer='developer')

    def test_str(self):
        self.assertEqual(self.game_developer.__str__(), self.game_developer.developer)


class GamePublisherTestCase(TestCase):

    def setUp(self):
        self.game_publisher = GamePublisher.objects.create(publisher='publisher')

    def test_str(self):
        self.assertEqual(self.game_publisher.__str__(), self.game_publisher.publisher)


class GameTestCase(TestCase):

    def setUp(self):
        self.game = Game.objects.create(game='game')

    def test_str(self):
        self.assertEqual(self.game.__str__(), self.game.game)


class GamePlatformImageTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(game='game')
        game_platform = GamePlatform.objects.create(platform='platform')
        game_game_platform = GameGamePlatform.objects.create(
            game=game, gameplatform=game_platform
        )
        self.game_platform_image = GamePlatformImage.objects.create(
            gamegameplatform=game_game_platform
        )

    def test_str(self):
        str_ = self.game_platform_image.__str__()
        game_str = self.game_platform_image.gamegameplatform.game.game
        platform_str = self.game_platform_image.gamegameplatform.gameplatform.platform
        str_compare = f'{game_str} - {platform_str}'
        self.assertEqual(str_, str_compare)


class GameGamePlatformTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(game='game')
        game_platform = GamePlatform.objects.create(platform='platform')
        self.game_game_platform = GameGamePlatform.objects.create(
            game=game, gameplatform=game_platform
        )

    def test_str(self):
        str_ = self.game_game_platform.__str__()
        game_str = self.game_game_platform.game.game
        platform_str = self.game_game_platform.gameplatform.platform
        str_compare = f'{game_str} - {platform_str}'
        self.assertEqual(str_, str_compare)

    def test_get_default_image(self):
        self.game_platform_image_3_false = GamePlatformImage.objects.create(
            gamegameplatform=self.game_game_platform, default=False
        )
        self.game_platform_image_1_true = GamePlatformImage.objects.create(
            gamegameplatform=self.game_game_platform, default=True
        )
        self.game_platform_image_2_true = GamePlatformImage.objects.create(
            gamegameplatform=self.game_game_platform, default=True
        )
        default_image = self.game_game_platform.get_default_image()
        self.assertEqual(default_image, self.game_platform_image_1_true)
        self.assertNotEqual(default_image, self.game_platform_image_2_true)
        self.assertNotEqual(default_image, self.game_platform_image_3_false)

    def test_get_default_image_none(self):
        default_image = self.game_game_platform.get_default_image()
        self.assertIsNone(default_image)


class GameGameGenreTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(game='game')
        game_genre = GameGenre.objects.create(genre='genre')
        self.game_game_genre = GameGameGenre.objects.create(
            game=game, gamegenre=game_genre
        )


    def test_str(self):
        str_ = self.game_game_genre.__str__()
        game_str = self.game_game_genre.game.game
        genre_str = self.game_game_genre.gamegenre.genre
        str_compare = f'{game_str} - {genre_str}'
        self.assertEqual(str_, str_compare)


class GameMarketTestCase(TestCase):

    def setUp(self):
        user_model = get_user_model()
        user = user_model.objects.create(username='username')
        game = Game.objects.create(game='game')
        game_platform = GamePlatform.objects.create(platform='platform')    
        game_game_platform = GameGamePlatform.objects.create(
            game=game, gameplatform=game_platform
        )
        self.game_market = GameMarket.objects.create(
            user=user, gameplatform=game_game_platform, 
            action=GameMarket.ActionChoices.BUY, status=GameMarket.StatusChoices.ACTIVE
        )

    def test_str(self):
        str_ = self.game_market.__str__()
        user_str = self.game_market.user
        game_game_str = self.game_market.gameplatform
        str_compare = f'{user_str} - {game_game_str} ({self.game_market.get_action_display()})'
        self.assertEqual(str_, str_compare)
