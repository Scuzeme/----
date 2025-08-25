"""
Subscription Management System
Handles subscription creation, management, and cancellation
"""

from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import json


class SubscriptionStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"


class SubscriptionPlan(Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


@dataclass
class Subscription:
    """Subscription data model"""
    id: str
    user_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    created_at: datetime
    expires_at: datetime
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan': self.plan.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancellation_reason': self.cancellation_reason
        }


class SubscriptionManager:
    """Manages subscription operations"""
    
    def __init__(self):
        self.subscriptions: List[Subscription] = []
    
    def create_subscription(self, user_id: str, plan: SubscriptionPlan) -> Subscription:
        """Create a new subscription"""
        subscription_id = f"sub_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Set expiration based on plan (example durations)
        duration_days = {
            SubscriptionPlan.BASIC: 30,
            SubscriptionPlan.PREMIUM: 30,
            SubscriptionPlan.ENTERPRISE: 365
        }
        
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration_days[plan])
        
        subscription = Subscription(
            id=subscription_id,
            user_id=user_id,
            plan=plan,
            status=SubscriptionStatus.ACTIVE,
            created_at=created_at,
            expires_at=expires_at
        )
        
        self.subscriptions.append(subscription)
        return subscription
    
    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get subscription by ID"""
        for sub in self.subscriptions:
            if sub.id == subscription_id:
                return sub
        return None
    
    def get_user_subscriptions(self, user_id: str) -> List[Subscription]:
        """Get all subscriptions for a user"""
        return [sub for sub in self.subscriptions if sub.user_id == user_id]
    
    def cancel_subscription(self, subscription_id: str, reason: str = None) -> bool:
        """Cancel a subscription"""
        subscription = self.get_subscription(subscription_id)
        
        if not subscription:
            print(f"Subscription {subscription_id} not found")
            return False
        
        if subscription.status == SubscriptionStatus.CANCELLED:
            print(f"Subscription {subscription_id} is already cancelled")
            return False
        
        # Update subscription status
        subscription.status = SubscriptionStatus.CANCELLED
        subscription.cancelled_at = datetime.now()
        subscription.cancellation_reason = reason or "User requested cancellation"
        
        print(f"Successfully cancelled subscription {subscription_id}")
        print(f"Cancellation date: {subscription.cancelled_at}")
        print(f"Reason: {subscription.cancellation_reason}")
        
        return True
    
    def list_subscriptions(self) -> List[dict]:
        """List all subscriptions"""
        return [sub.to_dict() for sub in self.subscriptions]
    
    def save_to_file(self, filename: str = "subscriptions.json"):
        """Save subscriptions to JSON file"""
        data = self.list_subscriptions()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Subscriptions saved to {filename}")
    
    def load_from_file(self, filename: str = "subscriptions.json"):
        """Load subscriptions from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.subscriptions = []
            for item in data:
                sub = Subscription(
                    id=item['id'],
                    user_id=item['user_id'],
                    plan=SubscriptionPlan(item['plan']),
                    status=SubscriptionStatus(item['status']),
                    created_at=datetime.fromisoformat(item['created_at']),
                    expires_at=datetime.fromisoformat(item['expires_at']),
                    cancelled_at=datetime.fromisoformat(item['cancelled_at']) if item['cancelled_at'] else None,
                    cancellation_reason=item['cancellation_reason']
                )
                self.subscriptions.append(sub)
            
            print(f"Loaded {len(self.subscriptions)} subscriptions from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found, starting with empty subscription list")
        except Exception as e:
            print(f"Error loading subscriptions: {e}")


def main():
    """Demo/CLI interface for subscription management"""
    manager = SubscriptionManager()
    
    # Try to load existing subscriptions
    manager.load_from_file()
    
    print("=== Subscription Management System ===")
    print("Commands:")
    print("1. create <user_id> <plan> - Create subscription (plan: basic/premium/enterprise)")
    print("2. cancel <subscription_id> [reason] - Cancel subscription")
    print("3. list - List all subscriptions")
    print("4. user <user_id> - List subscriptions for user")
    print("5. save - Save subscriptions to file")
    print("6. quit - Exit")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().split()
            
            if not command:
                continue
                
            action = command[0].lower()
            
            if action == "quit":
                break
            elif action == "create" and len(command) >= 3:
                user_id = command[1]
                plan_str = command[2].lower()
                
                try:
                    plan = SubscriptionPlan(plan_str)
                    sub = manager.create_subscription(user_id, plan)
                    print(f"Created subscription: {sub.id}")
                except ValueError:
                    print("Invalid plan. Use: basic, premium, or enterprise")
                    
            elif action == "cancel" and len(command) >= 2:
                sub_id = command[1]
                reason = " ".join(command[2:]) if len(command) > 2 else None
                manager.cancel_subscription(sub_id, reason)
                
            elif action == "list":
                subs = manager.list_subscriptions()
                if not subs:
                    print("No subscriptions found")
                else:
                    print(f"\nFound {len(subs)} subscriptions:")
                    for sub in subs:
                        print(f"ID: {sub['id']}")
                        print(f"  User: {sub['user_id']}")
                        print(f"  Plan: {sub['plan']}")
                        print(f"  Status: {sub['status']}")
                        print(f"  Created: {sub['created_at']}")
                        if sub['cancelled_at']:
                            print(f"  Cancelled: {sub['cancelled_at']}")
                            print(f"  Reason: {sub['cancellation_reason']}")
                        print()
                        
            elif action == "user" and len(command) >= 2:
                user_id = command[1]
                subs = manager.get_user_subscriptions(user_id)
                if not subs:
                    print(f"No subscriptions found for user {user_id}")
                else:
                    print(f"\nSubscriptions for user {user_id}:")
                    for sub in subs:
                        print(f"  {sub.id} - {sub.plan.value} ({sub.status.value})")
                        
            elif action == "save":
                manager.save_to_file()
                
            else:
                print("Invalid command or missing parameters")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Save before exit
    manager.save_to_file()
    print("Goodbye!")


if __name__ == "__main__":
    main()