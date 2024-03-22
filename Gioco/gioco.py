import pygame
import sys

pygame.init()

window_white = (0, 0, 0)
window_width = 800
window_height = 600
victory_text = "Hai vinto"

window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Gioco Negro")

uovo = pygame.image.load("egg.png")
shop = pygame.image.load("store.png")
upgrade = pygame.image.load("upgrade_prompt.png")
shopwindow = False
settingswindow = False

shop = pygame.transform.scale(shop, (upgrade.get_width() // 3, upgrade.get_height() // 3))
shop_pos = (30, 30) 

pygame.display.set_icon(uovo)

click_font = pygame.font.Font(None, 36)
click_count = 0
click_multiplier = 1
egg_sfx = pygame.mixer.Sound("sound.mp3")
upgrade_sfx = pygame.mixer.Sound("porcodio.mp3")
background_sfx = pygame.mixer.Sound("musicasfondo.mp3")
victory_sfx = pygame.mixer.Sound("victory.mp3")
channelbg = pygame.mixer.Channel(0)
ChannelPorcodio = pygame.mixer.Channel(1)
ChannelMain = pygame.mixer.Channel(2)

victory = 1000
upgrade_prompt = pygame.image.load("upgrade_prompt.png")
upgrade_prompt = pygame.transform.scale(upgrade_prompt, (175, 150))
upgrade_prompt_rect = upgrade_prompt.get_rect(topleft=(window_width - upgrade_prompt.get_width() - 30, 30))
upgraded_times = 1



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            egg_rect = uovo.get_rect()
            egg_rect.center = (window_width / 2, window_height / 2)
            if egg_rect.collidepoint(event.pos) and not shopwindow: 
                ChannelMain.play(egg_sfx)
                click_count += click_multiplier
            if click_count >= (100 * upgraded_times) and upgrade_prompt_rect.collidepoint(event.pos) and not shopwindow:  
                click_count -= (100 * upgraded_times)
                click_multiplier += 1
                upgraded_times += 1
                ChannelPorcodio.play(upgrade_sfx)
        elif event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    upgrade_prompt_rect.topleft = (window_width - upgrade_prompt.get_width() - 30, 30)
    window.fill(window_white)

    
    
    settings = pygame.image.load("settings.png")
    settings_rect = settings.get_rect(topleft=(window_width - 30, window_height - 30))
    if event.type == pygame.MOUSEBUTTONDOWN:
        if settings_rect.collidepoint(event.pos):
            settingswindow = True
            eventtype = pygame.MOUSEBUTTONDOWN
    window.blit(settings, settings_rect)
    

    if not shopwindow:  
        window.blit(uovo, (window_width / 2 - uovo.get_width() / 2, window_height / 2 - uovo.get_height() / 2))

    click_text = click_font.render(f"Clicks: {click_count}", True, (255, 255, 255))
    click_text_rect = click_text.get_rect()
    click_text_rect.topleft = (window_width / 2 + uovo.get_width() / 2, window_height / 2 - click_text_rect.height / 2)
    window.blit(click_text, click_text_rect)
    if click_count >= (100 * upgraded_times) and not shopwindow: 
        abcdef = 0
    shop_rect = shop.get_rect(topleft=shop_pos)
    if click_count >= victory:
        victory_text = click_font.render("Hai vinto", True, (255, 255, 255))
        victory_text_rect = victory_text.get_rect(topleft=(window_width / 2 - victory_text.get_width() / 2,
                                                           window_height / 2 - victory_text.get_height() / 2 - 175))
        window.blit(victory_text, victory_text_rect)
        victory_sfx.play()

    window.blit(shop, shop_pos) 
    if event.type == pygame.MOUSEBUTTONDOWN:
        if shop_rect.collidepoint(event.pos):
            shopwindow = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if shopwindow and not shop_rect.collidepoint(event.pos):  
            shopwindow = False
    if shopwindow:
        window.fill(window_white)
        shop_window_text = click_font.render("Shop Window", True, (255, 255, 255))
        shop_window_text_rect = shop_window_text.get_rect(topleft=(window_width / 2 - shop_window_text.get_width() / 2, 30))
        window.blit(shop_window_text, shop_window_text_rect)
        window.blit(upgrade_prompt, upgrade_prompt_rect)
        if click_count < (100 * upgraded_times):
            not_enough_money_text = click_font.render("Not enough money", True, (255, 0, 0))
            not_enough_money_text_rect = not_enough_money_text.get_rect(midright=(window_width - 15, window_height / 2 - 80))
            window.blit(not_enough_money_text, not_enough_money_text_rect)
    pygame.display.flip()
    if click_count >= 100 and shopwindow == True:
        upgrade_prompt_rect.topright = (window_width - 30, 30)
        if click_count >= (100 * upgraded_times) and shopwindow == True:
            upgrade_prompt_rect.topleft = (window_width // 2 - upgrade_prompt.get_width() // 2, window_height // 2 - upgrade_prompt.get_height() // 2)
            window.blit(upgrade_prompt, upgrade_prompt_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if upgrade_prompt_rect.collidepoint(window_width - upgrade_prompt.get_width() - 30, 30):
                    click_count -= (100 * upgraded_times)
                    click_multiplier += 1
                    upgraded_times += 1
                    ChannelPorcodio.play(upgrade_sfx)
    if shopwindow == True:
        window.fill(window_white)
        shop_window_text = click_font.render("Shop Window", True, (255, 255, 255))
        shop_window_text_rect = shop_window_text.get_rect(topleft=(window_width - 30, window_height - 30))
        window.blit(shop_window_text, shop_window_text_rect)
        if click_count >= (100*click_multiplier) and click_count >= (100 * upgraded_times):
            upgrade_prompt_rect.topright = (window_width - 30, 30)
            window.blit(upgrade_prompt, upgrade_prompt_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and click_count >= (100 * upgraded_times):
            if upgrade_prompt_rect.collidepoint(event.pos) and click_count >= (100 * upgraded_times):
                click_count -= (100 * upgraded_times)
                click_multiplier += 1
                upgraded_times += 1
                ChannelPorcodio.play(upgrade_sfx)
            elif event.type == pygame.MOUSEBUTTONUP and click_count >= (100 * upgraded_times):
                if upgrade_prompt_rect.collidepoint(event.pos) and click_count >= (100 * upgraded_times):
                    click_count -= (100 * upgraded_times)
                    click_multiplier += 1
                else:
                    pygame.display.flip()    


sys.exit()


