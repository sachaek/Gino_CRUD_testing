from gino import Gino
import asyncio

# postgres:
login = "postgres"
password = "root"

db = Gino()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')



async def main():
    await db.set_bind('postgresql://postgres:root@localhost/gino')
    print(db.is_bound())
    await db.gino.create_all()

    # user = await User.create(nickname='fantix') # создание 1
    # user = User(nickname='fantix') # создание 2
    # user.nickname += ' (founder)' # создание 2
    # await user.create() # создание 2

    result = await db.select([User.id, User.nickname]).gino.all()

    print(result)
    # print(f'ID:       {user.id}')
    # print(f'Nickname: {user.nickname}')
    print('////////////////////////////////')
    user = await User.get(71)
    print(user.nickname, 'number 71 from get')

    print('////////////////////////////////')
    all_users = await db.all(User.query)
    list_users = []
    for user in all_users:
        list_users.append(user.nickname)
    print(list_users)

    all_users = await User.query.gino.all()
    list_users = []
    for user in all_users:
        list_users.append(user.nickname)
    print(list_users)
    print('////////////////////////////////')

    print('////////////////////////////////')
    founding_users = await User.query.where(User.id > 10).gino.all()
    founding_users_list = list()
    for user in founding_users:
        founding_users_list.append(str(user.nickname)+str(user.id))
    print(founding_users_list)

    print('//////////////////////////////// using .first()  ')
    user = await User.query.where(User.id < 10).gino.first()
    print(user.id)

    print('//////////////////////////////// select; just single value')
    name = await User.select('nickname').where(User.id == 1).gino.scalar()
    # SQL (parameter: 1):
    # SELECT users.nickname FROM users WHERE users.id = $1
    print(name)  # fantix

    print('//////////////////////////////// just count rows')
    population = await db.func.count(User.id).gino.scalar()
    # SQL:
    # SELECT count(users.id) AS count_1 FROM users
    print(population)  # 17 for example

    print('//////////////////////////////// update here: ')
    user = await User.query.where(User.id == 2).gino.first() # change id for result
    name_before = str(user.nickname)
    await user.update(nickname='daisy').apply()
    user = await User.query.where(User.id == 2).gino.first()
    name_after = str(user.nickname)
    print(f'{name_before=}, {name_after=}')

    print('//////////////////////////////// AND deleting: ')
    user = await User.create(nickname='fantix')
    await user.delete()
    # SQL (parameter: 1):
    # DELETE FROM users WHERE users.id = $1
    print(await User.get(user.id))  # None


    # in the end
    await db.pop_bind().close() # disconnect from the database




if __name__ == "__main__":
    asyncio.run(main())
