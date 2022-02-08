from django.db import models
from stdimage.models import StdImageField
from django.core.validators import MaxValueValidator


class GameGenre(models.Model):
    genre = models.CharField('Genre', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Game Genre'
        verbose_name_plural = 'Game Genres'

    def __str__(self):
        return self.genre


class GamePlatform(models.Model):
    platform = models.CharField('Platform', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Game Platform'
        verbose_name_plural = 'Game Platforms'

    def __str__(self):
        return self.platform


class GameDeveloper(models.Model):
    developer = models.CharField('Developer', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Game Developer'
        verbose_name_plural = 'Game Developers'

    def __str__(self):
        return self.developer


class GamePublisher(models.Model):
    publisher = models.CharField('Publisher', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Game Publisher'
        verbose_name_plural = 'Game Publishers'

    def __str__(self):
        return self.publisher


class Game(models.Model):
    game = models.CharField('Game', max_length=50, unique=True)
    genre = models.ManyToManyField('GameGenre', blank=True, verbose_name='Genre', through='GameGameGenre')
    platform = models.ManyToManyField('GamePlatform', blank=True, verbose_name='Platform', through='GameGamePlatform')
    description = models.TextField('Description', blank=True)
    developer = models.ForeignKey('GameDeveloper', verbose_name='Developer', on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey('GamePublisher', verbose_name='Publisher', on_delete=models.SET_NULL, null=True, blank=True)
    age_rating = models.PositiveSmallIntegerField('Age Rating', null=True, blank=True, validators=[MaxValueValidator(18)])
    
    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.game


def image_upload_path(instance, filename):
    return 'games/platforms/{0}_{1}'.format(instance.gamegameplatform.id, filename)


class GamePlatformImage(models.Model):
    gamegameplatform = models.ForeignKey('GameGamePlatform', on_delete=models.CASCADE)
    image = StdImageField('Image', upload_to=image_upload_path, variations={'thumbnail': {'width': 117, 'height': 147, 'crop': False}}, delete_orphans=True)
    default = models.BooleanField('Default', default=False)

    def __str__(self):
        return f'{self.gamegameplatform.game.game} - {self.gamegameplatform.gameplatform.platform}'


class GameGamePlatform(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    gameplatform = models.ForeignKey('GamePlatform', on_delete=models.CASCADE)
    metascore = models.PositiveSmallIntegerField('Metascore', null=True, blank=True, validators=[MaxValueValidator(100)])
    release_date = models.DateField('Release Date', null=True, blank=True)

    def get_default_image(self):
        return GamePlatformImage.objects.filter(gamegameplatform=self.pk, default=True).first()

    class Meta:
        db_table = 'bstgames_game_platform'
        constraints = [
            models.UniqueConstraint(name='unique_game_gameplatform', fields=['game', 'gameplatform'])
        ]

    def __str__(self):
        return f'{self.game.game} - {self.gameplatform.platform}'


class GameGameGenre(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    gamegenre = models.ForeignKey('GameGenre', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bstgames_game_genre'
        constraints = [
            models.UniqueConstraint(name='unique_game_gamegenre', fields=['game', 'gamegenre'])
        ]

    def __str__(self):
        return f'{self.game.game} - {self.gamegenre.genre}'


class GameMarket(models.Model):
    
    class ActionChoices(models.IntegerChoices):
        BUY = 1, 'Buy'
        SELL = 2, 'Sell'
        TRADE = 3, 'Trade'

    class StatusChoices(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        INACTIVE = 2, 'Inactive'
        
    user = models.ForeignKey('users.User', verbose_name='User', on_delete=models.CASCADE)
    gameplatform = models.ForeignKey('GameGamePlatform', verbose_name='Game - Platform', on_delete=models.CASCADE, null=True)
    action = models.PositiveSmallIntegerField('Action', choices=ActionChoices.choices)
    trade = models.ManyToManyField('GameGamePlatform', blank=True, verbose_name='Trade For', related_name='trades')
    status = models.PositiveSmallIntegerField('Status', choices=StatusChoices.choices)
    price = models.DecimalField('Price', max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Game Market'
        verbose_name_plural = 'Game Markets'

    def __str__(self):
        return f'{self.user} - {self.gameplatform} ({self.get_action_display()})'
