from asgiref.sync import sync_to_async
from botapp.models import BotUser
from documents.models import Contract
from django.core.files.base import ContentFile
import logging

class DBcommands:
    @sync_to_async
    def add_user(self, user_id: int, full_name: str, username: str|None ):
        user, created = BotUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                'username': username,
                'full_name': full_name
            }
        )
        response = {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'is_checked': user.is_checked,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'created': created
        }
        if created:
            logging.info(f"New user was added to the database: {response}")
        return response
    
    @sync_to_async
    def check_user(self, user_id: int):
        try:
            user = BotUser.objects.get(user_id=user_id)
            user.is_checked = True
            user.save()
            return user.is_checked
        except BotUser.DoesNotExist:
            return False
    

    @sync_to_async
    def get_user_check(self, user_id: int):
        try:
            user = BotUser.objects.get(user_id=user_id)
            return user.is_checked
        except BotUser.DoesNotExist:
            return False
        
    
    @sync_to_async
    def logout_user(self, user_id: int):
        try:
            user = BotUser.objects.get(user_id=user_id)
            user.is_checked = False
            user.save()
            return True
        except BotUser.DoesNotExist:
            return False
        
    
    @sync_to_async
    def create_contract(self, user_id: int, data: dict):
        """
        Create a new contract
        Parameters:
        user_id: int - user id
        data: dict - contract data
        {
            "company_owner": str,
            "company_name": str,
            "total_price": str,
            "monthly_payment": str,
            "company_address": str,
            "company_account": str,
            "company_bank": str,
            "company_mfo": str,
            "company_inn": str,
            "company_oked": str,
            "company_phone": str,
            "contact_phone": str,
            "pdf_file": bytes
        }

        """

        try:
            user = BotUser.objects.get(user_id=user_id)
            contract = Contract.objects.create(
                user=user,
                director_name=data['company_owner'],
                company_name=data['company_name'],
                total_price=data['summa'],
                monthly_payment=data['month_summa'],
                company_address=data['company_address'],
                company_account=data['company_account'],
                company_bank=data['company_bank'],
                company_mfo=data['company_mfo'],
                company_inn=data['company_inn'],
                company_oked=data['company_oked'],
                company_phone=data['company_phone'],
                contact_phone=data['contact_phone'],
            )
            contract.pdf_file.save(f'{data["company_name"]}_N{contract.id}-contract.pdf', ContentFile(data['pdf_file']), save=True)
            return contract.id
        except BotUser.DoesNotExist:
            logging.error(f"User with id {user_id} do not found while creating a contract")
            return False
    

    @sync_to_async
    def change_status_contract(self, contract_id: int, status: str):
        try:
            contract = Contract.objects.get(id=contract_id)
            contract.status = status
            contract.save()
            return True
        except Contract.DoesNotExist:
            logging.error(f"Contract with id {contract_id} do not found while changing status")
            return False