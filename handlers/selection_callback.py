from aiogram import F, Router, types


router = Router()


@router.callback_query(F.data.startswith("selection_"))
async def callbacks_selection(callback: types.CallbackQuery) -> None:
    await callback.message.answer(f"Вы выбрали {callback.data.split('_')[1]}")
