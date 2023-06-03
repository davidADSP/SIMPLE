import pygame
from pygame.locals import *
import os
from classes.board import Board
from classes.town import Town
from classes.player import Player
from classes.build_location import BuildLocation
from classes.buildings.enums import BuildingName
import asyncio
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 24)

WIDTH = 1200
HEIGHT = 1200
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
ORANGE = (255, 153, 51)
BLUE = (87,155,252)
GREY = (100, 100, 100)
TAN = (229, 156, 91)

BEER_SIZE = 12

PLAYER_COLOR_MAP = {
	"Red": RED,
	"Blue": BLUE,
	"Green": GREEN,
	"Yellow": YELLOW
}

#flipped building colors
PLAYER_BUILDING_RETIRED_COLOR_MAP = {
	"Red": (84, 0, 0),
	"Blue": (0, 0, 84),
	"Green": (4, 84, 0),
	"Yellow": (85, 72, 0)
}

MARGIN = 50

BUILDING_COORDS = {'Leek': [[632, 92], [687, 92]], 'Stoke-On-Trent': [[492, 125], [467, 177], [522, 177]], 'Stone': [[342, 302], [397, 302]], 'Uttoxeter': [[647, 282], [702, 282]], 'Belper': [[847, 127], [902, 127], [957, 127]], 'Derby': [[905, 255], [877, 307], [932, 307]], 'Stafford': [[452, 412], [507, 412]], 'Burton-Upon-Trent': [[787, 447], [842, 447]], 'beer1': [[357, 522]], 'Cannock': [[537, 532], [592, 532]], 'Tamworth': [[802, 597], [857, 597]], 'Walsall': [[607, 672], [662, 672]], 'Coalbrookdale': [[282, 637], [252, 697], [307, 697]], 'Wolverhampton': [[417, 642], [472, 642]], 'Dudley': [[472, 787], [527, 787]], 'Kidderminster': [[387, 912], [442, 912]], 'beer2': [[292, 997]], 'Worcester': [[402, 1062], [457, 1062]], 'Birmingham': [[722, 777], [777, 777], [722, 832], [777, 832]], 'Nuneaton': [[912, 712], [967, 712]], 'Coventry': [[967, 812], [937, 872], [992, 872]], 'Redditch': [[667, 972], [722, 972]]}

TRADE_POST_COORDS = {
	"Warrington": [
		[290, 150],
		[345, 150]
	],
	"Nottingham": [
		[1040, 215],
		[1105, 215]
	],
	"Shrewbury": [
		[95, 715]
	],
	"Oxford": [
		[945, 1020],
		[1000, 1020]
	],
	"Gloucester": [
		[680, 1110],
		[735, 1110]
	],
}

BEER_COORDS = {
	"Warrington": [
		(290, 205),
		(369, 206)
	],
	"Nottingham": [
		(1049, 271),
		(1125, 275)
	],
	"Shrewbury": [
		(150, 713)
	],
	"Oxford": [
		(946, 986),
		(1023, 987),
	],
	"Gloucester": [
		(682, 1073),
		(765, 1072),
	],
}

ROAD_LOCATION_COORDS = [
	[422, 120], 	#[WARRINGTON, STOKE_ON_TRENT]
	[564, 107], 	#[STOKE_ON_TRENT, LEEK]
	[770, 92], 		#[LEEK, BELPER], False
	[918, 206], 	#[BELPER, DERBY]
	[980, 253], 	#[DERBY, NOTTINGHAM]
	[792, 305], 	#[DERBY, UTTOXETER], False
	[899, 401], 	#[DERBY, BURTON_UPON_TRENT]
	[444, 256], 	#[STOKE_ON_TRENT, STONE]
	[519, 293], 	#[STONE, UTTOXETER], False
	[383, 402], 	#[STONE, STAFFORD]
	[622, 359], 	#[STONE, BURTON_UPON_TRENT]
	[569, 469], 	#[STAFFORD, CANNOCK]
	[686, 477], 	#[CANNOCK, BURTON_UPON_TRENT], False
	[836, 527], 	#[TAMWORTH, BURTON_UPON_TRENT]
	[703, 562], 	#[WALSALL, BURTON_UPON_TRENT], canBuildRailroad=False
	[462, 520], 	#[BEER1, CANNOCK]
	[478, 577], 	#[WOLVERHAMPTON, CANNOCK]
	[645, 597], 	#[WALSALL, CANNOCK]
	[353, 644], 	#[WOLVERHAMPTON, COALBROOKDALE]
	[203, 644], 	#[SHREWBURY, COALBROOKDALE]
	[319, 827], 	#[KIDDERMINSTER, COALBROOKDALE]
	[428, 849], 	#[KIDDERMINSTER, DUDLEY]
	[545, 654], 	#[WOLVERHAMPTON, WALSALL]
	[450, 730], 	#[WOLVERHAMPTON, DUDLEY]
	[743, 661], 	#[TAMWORTH, WALSALL], False
	[930, 630], 	#[TAMWORTH, NUNEATON]
	[1025, 780], 	#[NUNEATON, COVENTRY]
	[663, 759], 	#[BIRMINGHAM, WALSALL]
	[834, 699], 	#[BIRMINGHAM, TAMWORTH]
	[856, 763], 	#[BIRMINGHAM, NUNEATON], False
	[858, 861], 	#[BIRMINGHAM, COVENTRY]
	[856, 916], 	#[BIRMINGHAM, OXFORD]
	[735, 913], 	#[BIRMINGHAM, REDDITCH], False
	[577, 948], 	#[BIRMINGHAM, WORCESTER]
	[610, 803], 	#[BIRMINGHAM, DUDLEY]
	[797, 994], 	#[REDDITCH, OXFORD]
	[604, 1025], 	#[REDDITCH, GLOUCESTER]
	[526, 1101], 	#[WORCESTER, GLOUCESTER]
	[407, 996], 	#[WORCESTER, BEER2, KIDDERMINSTER]
]

DECK_POSITION = (170, 190)
CARD_WIDTH = 130
CARD_HEIGHT = 180


class Render:
	def __init__(self, board=None, callback=None, x=0, y=0):
		local_dir = os.path.dirname(__file__)
		self.board = board
		self.callback = callback
		self.img = pygame.image.load(f'{local_dir}/render/board.jpg')
		self.goldCard = pygame.image.load(f"{local_dir}/render/gold-card.png")
		self.greyCard = pygame.image.load(f"{local_dir}/render/grey-card.png")
		self.greyCard = pygame.transform.scale(self.greyCard, (CARD_WIDTH, CARD_HEIGHT))
		self.goldCard = pygame.transform.scale(self.goldCard, (CARD_WIDTH, CARD_HEIGHT))
		self.greyCard = pygame.transform.rotate(self.greyCard, 90)
		self.goldCard = pygame.transform.rotate(self.goldCard, 90)
		self.win = pygame.display.set_mode((WIDTH, HEIGHT))
		self.x = x
		self.y = y
		self.frame = Rect(MARGIN/2, MARGIN/2, WIDTH-MARGIN, HEIGHT-MARGIN)
		self.running = True

		self.draw()

	def createGame(self, numPlayers, p1Name="Noah", p2Name="Tyler", p3Name="Sam", p4Name="Mr. McDonald"):
		self.board = Board(numPlayers)
		self.p1 = Player(p1Name, self.board)

		self.p2 = Player(p2Name, self.board)
		if numPlayers > 2:
			self.p3 = Player(p3Name, self.board)
		if numPlayers > 3:
			self.p4 = Player(p4Name, self.board)

	def drawMoney(self):
		x = 10
		y = 10
		rect = Rect(5, 5, 100, 100)
		pygame.draw.rect(self.win, WHITE, rect)
		for player in self.board.players:
			img = font.render(f"{player.name}: ${player.money}", True,  PLAYER_COLOR_MAP[player.color])
			self.win.blit(img, (x, y))
			y += 20

	def drawTradingPostBeer(self):
		for trade in self.board.tradePosts:
			coords = BEER_COORDS[trade.name]
			if trade.beerAmount > 0:
				pygame.draw.circle(self.win, TAN, coords[0], BEER_SIZE)
			if trade.beerAmount > 1:
				pygame.draw.circle(self.win, TAN, coords[1], BEER_SIZE)

	def drawMerchantTiles(self):
		for trade in self.board.tradePosts:
			coords = TRADE_POST_COORDS[trade.name]
			if len(trade.merchantTiles) > 0:
				x, y = coords[0]
				
				rect = Rect(x, y, 30, 30)
				pygame.draw.rect(self.win, BLUE, rect)
				img = font.render(f"{trade.merchantTiles[0].value}", True, WHITE)
				self.win.blit(img, (x-23, y))

			if len(trade.merchantTiles) > 1:
				x, y = coords[1]
				
				rect = Rect(x, y, 30, 30)
				pygame.draw.rect(self.win, BLUE, rect)
				img = font.render(f"{trade.merchantTiles[1].value}", True, WHITE)
				self.win.blit(img, (x-23, y))

	def drawRoads(self):
		for i, road in enumerate(self.board.roadLocations):
			if road.isBuilt:
				coords = ROAD_LOCATION_COORDS[i]
				x, y = coords

				pygame.draw.circle(self.win, PLAYER_COLOR_MAP[road.road.owner.color], coords, 10)
				# if i % 2 == 0:
				# 	img = font.render(f"{road.towns[0].name}, {road.towns[1].name}", True, WHITE)
				# else:
				# 	img = font.render(f"{road.towns[0].name}, {road.towns[1].name}", True, RED)
				# self.win.blit(img, (x, y))

	def drawBuildings(self):
		for town in self.board.towns:
			for buildLocation in town.buildLocations:
				if buildLocation.building:
					self.drawBuilding(buildLocation)

	#draw BUILT 
	def drawBuilding(self, buildLocation: BuildLocation):
		# print(f"{buildLocation.id=}")
		x, y = None, None
		coords = BUILDING_COORDS[buildLocation.town.name]
		for i, location in enumerate(buildLocation.town.buildLocations):
			if buildLocation.id == location.id:
				x, y = coords[i]
		
		rect = Rect(x-22, y-22, 50, 50)
		
		if buildLocation.building.isFlipped:
			color = PLAYER_BUILDING_RETIRED_COLOR_MAP[buildLocation.building.owner.color]
			textColor = GREY
		else:
			color = PLAYER_COLOR_MAP[buildLocation.building.owner.color]
			textColor = WHITE

		pygame.draw.rect(self.win, color, rect)
		img = font.render(f"{buildLocation.building.name.value}", True, textColor)
		self.win.blit(img, (x-23, y-10))

	def drawCoal(self):
		for i in range(self.board.coalMarketRemaining):
			x = 1000
			if i % 2 == 0:
				x += 25
			y = 385 + (i//2*35.5)
			rect = Rect(x, y, 15, 15)
			pygame.draw.rect(self.win, BLACK, rect)
		img = font.render(f"{self.board.coalMarketRemaining}", True, BLACK)
		self.win.blit(img, (1000, 330))

	def drawIron(self):
		for i in range(self.board.ironMarketRemaining):
			x = 1065
			if i % 2 == 0:
				x += 25
			y = 458 + (i//2*35.5)
			rect = Rect(x, y, 15, 15)
			pygame.draw.rect(self.win, ORANGE, rect)
		img = font.render(f"{self.board.ironMarketRemaining}", True, ORANGE)
		self.win.blit(img, (1100, 400))

	def drawDeck(self):
		x, y = DECK_POSITION
		for i in range(len(self.board.deck.cards)):
			self.win.blit(self.greyCard, (x-(i*.5)-90, y-(i*.5)-70))
			# pygame.draw.circle(self.win, WHITE, (x, y), 5)
	
	def drawResourcesOnBuildings(self):
		for building in self.board.getCoalBuildings():
			coords = BUILDING_COORDS[building.town.name]
			for i, location in enumerate(building.town.buildLocations):
				if building.buildLocation.id == location.id:
					x, y = coords[i]
				
			startX = x

			assert building.resourcesType.name == "coal"
			for i in range(building.resourceAmount):
				if i > 0 and i % 3 == 0:
					y += 30
				x = startX + (i % 3) * 18

				# y += i//2*18
				rect = Rect(x-23, y-23, 15, 15)
				pygame.draw.rect(self.win, BLACK, rect)

		for building in self.board.getIronBuildings():
			coords = BUILDING_COORDS[building.town.name]
			for i, location in enumerate(building.town.buildLocations):
				if building.buildLocation.id == location.id:
					x, y = coords[i]
				
			startX = x

			print(building)
			print(building.resourcesType.name)
			assert building.resourcesType.name == "iron"
			for i in range(building.resourceAmount):
				if i > 0 and i % 3 == 0:
					y += 30
				x = startX + (i % 3) * 18

				# y += i//2*18
				rect = Rect(x-23, y-23, 15, 15)
				pygame.draw.rect(self.win, ORANGE, rect)

		for building in self.board.getBeerBuildings():
			coords = BUILDING_COORDS[building.town.name]
			for i, location in enumerate(building.town.buildLocations):
				if building.buildLocation.id == location.id:
					x, y = coords[i]
				
			startX = x

			assert building.resourcesType.name == "beer"
			for i in range(building.resourceAmount):
				if i > 0 and i % 3 == 0:
					y += 30
				x = startX + (i % 3) * 18

				# y += i//2*18
				pygame.draw.circle(self.win, TAN, (x+10, y+10), BEER_SIZE)

	async def drawWindow(self):
		while self.running:
			await asyncio.sleep(0.00001)
			self.win.fill((255, 255, 255))
			self.win.blit(self.win, (self.x, self.y))
			self.win.blit(self.img, (self.x, self.y))

			self.drawCoal()
			self.drawIron()
			self.drawMerchantTiles()
			self.drawRoads()
			self.drawDeck()
			self.drawBuildings()
			self.drawTradingPostBeer()
			self.drawMoney()
			self.drawResourcesOnBuildings()

			pygame.display.update()

	async def handleEvents(self):
		while self.running:
			await asyncio.sleep(0.00001)
			# event = pygame.event.wait()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					print(pygame.mouse.get_pos())

				# Did the user hit a key?
				if event.type == KEYDOWN:
					# Was it the Escape key? If so, stop the loop.
					if event.key == K_ESCAPE:
						self.running = False

				# Did the user click the window close button? If so, stop the loop.
				elif event.type == QUIT:
					self.running = False



	def draw(self):
		# animation_task = asyncio.ensure_future(self.drawWindow())
		# event_task = asyncio.ensure_future(self.handleEvents())
		# pygame_task = self.loop.run_in_executor(None, self.pygame_event_loop, self.loop, self.event_queue)
		# animation_task = self.loop.create_task(self.drawWindow())
		# event_task = self.loop.create_task(self.handleEvents())
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		coros = [self.drawWindow(), self.handleEvents()]
		if self.callback:
			coros.append(self.callback(self.board))
		loop.run_until_complete(asyncio.gather(*coros))
		# asyncio.run_coroutine_threadsafe(self.drawWindow(), loop)
		# asyncio.run_coroutine_threadsafe(self.handleEvents(), loop)
		# loop.close()

		# pygame.quit()
			
	async def main(self, loop):
		loop.create_task(self.drawWindow())
		loop.create_task(self.handleEvents())

def render(board, callback=None):
	Render(board, callback)