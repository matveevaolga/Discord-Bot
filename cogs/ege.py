import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from db_functions import get_task
from functions import date_to_days, get_days, embed_task_msg, embed_days_to_ege
from functions import find_channel_by_name
from row_buttons import RowButtons


class Ege(commands.Cog):
    '''ЕГЭ'''

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.slash_command(name='дней_до_егэ')
    async def ege_days(self, ctx):
        '''Дней до начала ЕГЭ'''

        inf = '2023-06-19'
        math = '2023-06-01'
        rus = '2023-05-29'
        physics = '2023-06-05'
        social = '2023-06-05'
        history = '2023-06-29'


        days_inf = date_to_days(inf)
        days_math = date_to_days(math)
        days_rus = date_to_days(rus)
        days_physics = date_to_days(physics)
        days_social = date_to_days(social)
        days_history = date_to_days(history)
        # окончания
        str_inf = get_days(days_inf + 1)
        str_math = get_days(days_math)
        str_rus = get_days(days_rus)
        str_physics = get_days(days_physics)
        str_social = get_days(days_social)
        str_history = get_days(days_history)

        t_ege = ((days_inf, str_inf), (days_math, str_math),
                 (days_rus, str_rus), (days_physics, str_physics),
                 (days_social, str_social), (days_history, str_history))

        title, description, color = embed_days_to_ege(t_ege)
        embed = disnake.Embed(
            title=title, description=description, color=color)

        #if int(days_rus) == 1:
        #    msg = 'Всем удачки на русском!\n Будьте котиками и затащите ^_^\n'
        #    msg += 'GTai с вами — сотка в кармане!'
        
        await ctx.send(embed=embed)
    

    @commands.slash_command(name='задачи_егэ_инф')
    async def tasks(self, 
     inter: disnake.ApplicationCommandInteraction,
    number_task: int = 8, complexity: str = 'Средняя'):
        '''Реши задачу из любого номера ЕГЭ по Информатике'''
        if str(inter.guild.get_channel(inter.channel.id)) == 'инфа-задачи' or \
                inter.author.display_name == 'GTai':
            lst_tasks = [2, 8]
            types_complexity = ['Лёгкая', 'Средняя', 'Сложная']
            complexity = complexity[0].upper() + complexity.lower()[1::]

            if number_task in lst_tasks and complexity in types_complexity:
                row = get_task(number_task, complexity)
                embed = embed_task_msg(number_task, row)

                await inter.send(embeds=embed, view=RowButtons(row['answer']))
            else:
                msg = f'Выбери номер из {lst_tasks} и сложность из {types_complexity}'
                await inter.send(msg)
        else:
            channel = find_channel_by_name(self.bot, 'инфа-задачи')
            msg = f'Задачи от меня ты можешь получить на канале {channel.mention}'
            await inter.send(msg)


    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='тест')
    async def test(self, inter: disnake.GuildCommandInteraction):
        #file = disnake.File(fp='S:/Programming/DB/ege_2/1.1.png')
        #embed = disnake.Embed(title='Test img',
        #    description='some text here')
        #embed.set_image(file=file)
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == 'вопросы-от-ведьмачки':
                    await inter.send(channel.mention)
        await inter.send(inter.author.display_name)


def setup(bot: commands.Bot):
    bot.add_cog(Ege(bot))