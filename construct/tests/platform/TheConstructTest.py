# from construct.platform.FundingStage import FundingStage
from construct.platform.FundingRoadmap import FundingRoadmap
# from construct.platform.SmartTokenShare import SmartTokenShare
from construct.platform.Milestone import Milestone
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments

from construct.platform.SmartTokenShareNew import SmartTokenShare, sts_create, sts_get 
from construct.platform.FundingStageNew import FundingStage, fs_create, fs_get, fs_contribute, fs_status


class TheConstructTest():
    """
    Test the TheConstruct from start to finish
    """

    project_id = 'projectID'
    symbol = 'PRO'
    decimals = 8
    owner = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
    total_supply = 10000000 * 100000000
    add_amount = 150

    funding_stage_id = 'funding_stage_id'
    start_block = 1
    end_block = 22000
    supply = 100000
    tokens_per_gas = 100
    



    def test(self, operation, args):

        
        # sts = SmartTokenShare()
        fr = FundingRoadmap()
        # fs = FundingStage()
        ms = Milestone()

        storage = StorageManager()
        attachments = get_asset_attachments()

        if operation == 'create_all':
            print('create_all')

            sts_create(self.project_id, self.symbol, self.decimals, self.owner, self.total_supply)
            fs_create(self.project_id, 'first_stage', 1, 99999, 1000, 100)
            fs_create(self.project_id, 'second_stage', 1, 99999, 500, 100)
            fs_create(self.project_id, 'third_stage', 1, 99999, 100, 100)
            fs_create(self.project_id, 'fourth_stage', 1, 99999, 200, 100)
            
            fss = ['first_stage', 'second_stage', 'third_stage', 'fourth_stage']

            ms.create(self.project_id, 'first_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'second_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'third_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'fourth_mile', 'First', 'sub', 'hash')
            
            mss = ['first_mile', 'second_mile', 'third_mile', 'fourth_mile']

            admins = [self.owner]

            fr.add_funding_stages(self.project_id, fss)
            fr.add_milestones(self.project_id, mss)
            fr.add_project_admins(self.project_id, admins)
            fr.set_active_index(self.project_id, 0)

            return True
            

        if operation == 'get_funding_stages':
            print('get_funding_stages')

            stages = fr.get_funding_stages(self.project_id)
            print(stages)

            return stages

        
        if operation == 'kyc':
            storage.put_triple(self.project_id, 'KYC_address', attachments.sender_addr, True)
          

        if operation == 'contribute':
            print('#contribute')
            # Registers KYC address
            storage.put_triple(self.project_id, 'KYC_address', attachments.sender_addr, True)
            
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]

            fs = fs_get(self.project_id, active_funding_stage)
            fs_contribute(fs)
            print('contribute#')

        if operation == 'get_idx':
            active_idx = fr.get_active_index(self.project_id)
            print(active_idx)
            return active_idx

        if operation == 'get_active_fs':
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            print(active_funding_stage)
            return active_funding_stage
        
        if operation == 'contribute_fs':
            print('#contribute_fs')

            active_funding_stage = args[0]
            
            fs = fs_get(self.project_id, active_funding_stage)
            fs_contribute(fs)
            
            print('contribute_fs#')
        
        
        if operation == 'balance':
            print('balance')
            bal = storage.get_double(self.project_id, attachments.sender_addr)
            print(bal)

        if operation == 'funding_stage_status':
            print('#funding_stage_status')
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            

            fs = fs_get(self.project_id, active_funding_stage)
            status = fs_status(fs)

            print('funding_stage_status#')
            print(status)
            return status

        if operation == 'current_index':
            active_idx = fr.get_active_index(self.project_id)
            print(active_idx)
            return active_idx
        
        if operation == 'milestone_progress':
            print('#milestone_progress')
            active_idx = fr.get_active_index(self.project_id)
            milestones = fr.get_milestones(self.project_id)
            active_milestone = milestones[active_idx]

            prog = ms.get_progress(self.project_id, active_milestone)
            print('milestone_progress#')
            print(prog)
            return prog

        if operation == 'complete_milestone':
            print('complete_milestone')
            fr.update_milestone_progress(self.project_id, 100)
            

        if operation == 'fs_supply':
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            
            fs = fs_get(self.project_id, active_funding_stage)
            # fs_info = fs.get_info(self.project_id, active_funding_stage)
            # supply = fs_info[fs.supply_idx]
            
            print(fs.supply)
            return fs.supply

        if operation == 'fs_circ':
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            
            fs = fs_get(self.project_id, active_funding_stage)

            # fs_info = fs.get_info(self.project_id, active_funding_stage)
            # supply = fs_info[fs.in_circulation_idx]
            print(fs.in_circulation)
            return fs.in_circulation

        if operation == 'sts_supply':
            sts = sts_get('projectID')
            supply = sts.total_supply

            print(supply)
            return supply

        if operation == 'sts_circ':
            sts = sts_get('projectID')
            in_circulation = sts.in_circulation

            print(in_circulation)
            return in_circulation

        return True