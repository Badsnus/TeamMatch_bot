from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import ShouldHaveArgs
from loader import dp
from models import Project, User
from services.projects import ArgsFields, parse_args
from services.profile import get_text_for_args_show_user
from services.project_profile import get_project_profile_text


@dp.message_handler(CommandStart(), ShouldHaveArgs(should_have=True))
async def show_some_profile_by_args(message: types.Message) -> None:
    try:
        name, id = parse_args(message.get_args())
    except Exception:
        await message.answer('<code>Что-то пошла не так :(</code>')
        return

    if name == ArgsFields.user.value:
        user = await User.get_user_with_projects(user_id=id)

        await message.answer(get_text_for_args_show_user(user))
        return
    try:
        project = await Project.get(project_id=id, do_join=True)
    except:  # TODO похер
        await message.answer('<code>Я не знаю такой проект :( </code>')
        return

    await message.answer_photo(
        caption=get_project_profile_text(project),
        photo=project.logo_image_id,
    )
