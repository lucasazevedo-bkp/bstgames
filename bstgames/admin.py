from django.contrib import admin
import nested_admin

from .models import (GameGenre, GamePlatform, GameDeveloper, 
    GamePublisher, Game, GameGameGenre, GameGamePlatform, 
    GameMarket, GamePlatformImage)
from .forms import GameGenreAdminForm, GamePlatformAdminForm

@admin.register(GameGenre)
class GameGenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)


@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ('platform',)


@admin.register(GameDeveloper)
class GameDeveloperAdmin(admin.ModelAdmin):
    list_display = ('developer',)


@admin.register(GamePublisher)
class GamePublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher',)


class GameGenreAdminInline(nested_admin.NestedTabularInline):
    model = GameGameGenre
    verbose_name = 'Genre'
    verbose_name_plural = 'Genres'
    form = GameGenreAdminForm

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            if obj.genre.count() > 0:
                extra = 0
        return extra


class GamePlatformImageAdminInline(nested_admin.NestedTabularInline):
    model = GamePlatformImage
    verbose_name = 'Platform Image'
    verbose_name_plural = 'Platform Images'

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            if obj.gameplatformimage_set.count() > 0:
                extra = 0
        return extra


class GamePlatformAdminInline(nested_admin.NestedStackedInline):
    model = GameGamePlatform
    verbose_name = 'Platform'
    verbose_name_plural = 'Platforms'
    form = GamePlatformAdminForm
    inlines = [GamePlatformImageAdminInline]

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            if obj.platform.count() > 0:
                extra = 0
        return extra
    

@admin.register(Game)
class GameAdmin(nested_admin.NestedModelAdmin):
    list_display = ('game', 'list_genre', 'list_platform')
    inlines = [GameGenreAdminInline, GamePlatformAdminInline]
    exclude = ('genre', 'platform')

    @admin.display(description='Genre')
    def list_genre(self, obj):
        if obj.genre.count():
            return ', '.join([g.genre for g in obj.genre.all()])
        return '-'

    @admin.display(description='Platform')
    def list_platform(self, obj):
        if obj.platform.count():
            return ', '.join([g.platform for g in obj.platform.all()])
        return '-'


@admin.register(GameMarket)
class GameMarketAdmin(admin.ModelAdmin):
    list_display = ('user', 'gameplatform', 'action', 'status', 'price', 'date')
    filter_horizontal = ('trade',)