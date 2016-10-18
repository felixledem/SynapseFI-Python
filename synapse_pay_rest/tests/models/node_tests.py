import unittest
import pdb
from synapse_pay_rest.tests.fixtures.client import *
from synapse_pay_rest.tests.fixtures.user import *
from synapse_pay_rest.tests.fixtures.node import *
from synapse_pay_rest.models.user import User
from synapse_pay_rest.models.node import Node
from synapse_pay_rest.models.nodes.ach_us_node import AchUsNode
from synapse_pay_rest.models.nodes.eft_ind_node import EftIndNode
from synapse_pay_rest.models.nodes.eft_np_node import EftNpNode
from synapse_pay_rest.models.nodes.iou_node import IouNode
from synapse_pay_rest.models.nodes.reserve_us_node import ReserveUsNode
from synapse_pay_rest.models.nodes.synapse_ind_node import SynapseIndNode
from synapse_pay_rest.models.nodes.synapse_np_node import SynapseNpNode
from synapse_pay_rest.models.nodes.synapse_us_node import SynapseUsNode
from synapse_pay_rest.models.nodes.wire_int_node import WireIntNode
from synapse_pay_rest.models.nodes.wire_us_node import WireUsNode


class NodeTestCases(unittest.TestCase):
    def setUp(self):
        self.client = test_client
        self.user = User.create(self.client, **user_create_args)

    def test_by_id(self):
        nodes = AchUsNode.create_via_bank_login(self.user, 'bofa',
                                                'synapse_nomfa', 'test1234')
        node_id = nodes[0].id
        node = Node.by_id(self.user, node_id)
        self.assertIsInstance(node, AchUsNode)
        self.assertEqual(node_id, node.id)

    def test_all(self):
        nodes = AchUsNode.create_via_bank_login(self.user, 'bofa',
                                                'synapse_nomfa', 'test1234')
        nodes = Node.all(self.user)
        self.assertEqual(2, len(nodes))
        self.assertIsInstance(nodes[0], AchUsNode)
        # with params
        per_page = 1
        page1 = Node.all(self.user, page=1, per_page=per_page)
        page2 = Node.all(self.user, page=2, per_page=per_page)
        self.assertNotEqual(page1[0].id, page2[0].id)
        self.assertEqual(per_page, len(page1))
        ach_nodes = Node.all(self.user, type='ACH-US')
        self.assertEqual(2, len(ach_nodes))
        synapse_nodes = Node.all(self.user, type='SYNAPSE-US')
        self.assertEqual(0, len(synapse_nodes))

    def test_deactivate(self):
        nodes = AchUsNode.create_via_bank_login(self.user, 'bofa',
                                                'synapse_nomfa', 'test1234')
        nodes = Node.all(self.user)
        self.assertEqual(2, len(nodes))
        nodes[0].deactivate()
        nodes = Node.all(self.user)
        self.assertEqual(1, len(nodes))
        nodes[0].deactivate()
        nodes = Node.all(self.user)
        self.assertEqual(0, len(nodes))

    def test_create_ach_us_via_account_and_routing(self):
        kwargs = {
            'account_number': '2345654323456754323',
            'routing_number': '051000017',
            'account_type': 'PERSONAL',
            'account_class': 'CHECKING',
            'supp_id': 'ABC123'
        }
        node = AchUsNode.create(self.user, 'Python Test ACH-US via Acct/Rt',
                                **kwargs)
        self.assertIsInstance(node, AchUsNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'bank_long_name', 'name_on_account', 'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_verify_node_microdeposits(self):
        pass

    def test_create_ach_us_via_bank_login_without_mfa(self):
        nodes = AchUsNode.create_via_bank_login(self.user, 'bofa',
                                                'synapse_nomfa', 'test1234')
        self.assertIsInstance(nodes, list)

        node = nodes[0]
        self.assertIsInstance(node, AchUsNode)
        other_props = ['user', 'id', 'type', 'is_active', 'bank_long_name',
                       'name_on_account', 'permission', 'bank_name', 'balance',
                       'currency', 'routing_number', 'account_number',
                       'account_class', 'account_type']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_ach_us_via_bank_login_with_mfa(self):
        pass

    def test_create_eft_ind_node(self):
        kwargs = {
          'ifsc': 'BKID0005046',
          'account_number': '2345654323456754323',
          'supp_id': 'ABC123'
        }
        node = EftIndNode.create(self.user, 'Python Test EFT-IND', **kwargs)
        self.assertIsInstance(node, EftIndNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_eft_np_node(self):
        kwargs = {
          'bank_name': 'Siddhartha Bank',
          'account_number': '2345654323456754323',
          'supp_id': 'ABC123'
        }
        node = EftNpNode.create(self.user, 'Python Test EFT-NP', **kwargs)
        self.assertIsInstance(node, EftNpNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_iou_node(self):
        kwargs = {
            'currency': 'USD',
            'supp_id': 'ABC123'
        }
        node = IouNode.create(self.user, 'Python Test IOU Node', **kwargs)
        self.assertIsInstance(node, IouNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_reserve_us_node(self):
        kwargs = {
            'supp_id': 'ABC123'
        }
        node = ReserveUsNode.create(self.user, 'Python Test RESERVE-US Node',
                                    **kwargs)
        self.assertIsInstance(node, ReserveUsNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission', 'balance', 'currency']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_synapse_ind_node(self):
        kwargs = {
            'supp_id': 'ABC123'
        }
        node = SynapseIndNode.create(self.user, 'Python Test SYNAPSE-IND Node',
                                     **kwargs)
        self.assertIsInstance(node, SynapseIndNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission', 'balance', 'currency', 'name_on_account']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_synapse_np_node(self):
        kwargs = {
            'supp_id': 'ABC123'
        }
        node = SynapseNpNode.create(self.user, 'Python Test SYNAPSE-NP Node',
                                    **kwargs)
        self.assertIsInstance(node, SynapseNpNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission', 'balance', 'currency', 'name_on_account']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_create_synapse_us_node(self):
        kwargs = {
            'supp_id': 'ABC123'
        }
        node = SynapseUsNode.create(self.user, 'Python Test SYNAPSE-US Node',
                                    **kwargs)
        self.assertIsInstance(node, SynapseUsNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission', 'balance', 'currency', 'name_on_account']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_wire_int_node(self):
        kwargs = {
            'bank_name': 'Bank of America',
            'account_number': '888888888',
            'routing_number': '051000017',
            'name_on_account': 'Medusa Pythonlady',
            'address': '123 Hiss Hiss',
            'correspondent_routing_number': '051000017',
            'correspondent_bank_name': 'Bank of America',
            'correspondent_address': '415 Donut Hiss at Me',
            'swift': 'TSIGFR22',
            'correspondent_swift': 'TSIGFR22',
            'supp_id': 'ABC123'
        }
        node = WireIntNode.create(self.user, 'Python Test WIRE-INT Node',
                                  **kwargs)
        self.assertIsInstance(node, WireIntNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))

    def test_create_wire_us_node(self):
        kwargs = {
            'bank_name': 'Bank of America',
            'account_number': '888888888',
            'routing_number': '051000017',
            'name_on_account': 'Medusa Pythonlady',
            'address': '123 Hiss Hiss',
            'correspondent_routing_number': '051000017',
            'correspondent_bank_name': 'Bank of America',
            'correspondent_address': '415 Donut Hiss at Me',
            'supp_id': 'ABC123'
        }
        node = WireUsNode.create(self.user, 'Python Test WIRE-US Node',
                                 **kwargs)
        self.assertIsInstance(node, WireUsNode)
        for prop in kwargs:
            self.assertIsNotNone(getattr(node, prop))

        other_props = ['user', 'nickname', 'id', 'type', 'is_active',
                       'permission']
        for prop in other_props:
            self.assertIsNotNone(getattr(node, prop))
