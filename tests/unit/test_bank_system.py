import pytest



def account_factory():
    """
    Helper function to create account
    """

def card_factory(account_id):
    """
    Helper function to register card to a user
    """
    


@pytest.mark.asyncio
async def test_create_user_account():
    """
    Test Account Creating Logic
    """

    #GIVEN
        
    #WHEN
        # Account Creating Logic
    #THEN
        # Assertion

@pytest.mark.asyncio
async def test_register_cards():

    #GIVEN
    _account = account_factory()

    #WHEN
        # Card Registration Logic
    #THEN
        # Assertion


@pytest.mark.asyncio
async def test_disable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Disabling Logic
    #THEN
        #Assertion

@pytest.mark.asyncio
async def test_enable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Enabling Logic
            
    #THEN
        #Assertion
            


@pytest.mark.asyncio
async def test_deposit_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Saving Logic

    #THEN

@pytest.mark.asyncio
async def test_withdraw_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Withdrawing Logic

    #THEN



@pytest.mark.asyncio
async def test_check_account_balance():
    ...
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Balace checking Logic
            
    #THEN
        #Assertion