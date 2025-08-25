#!/usr/bin/env python3
"""
Demo script to test subscription cancellation functionality
"""

from subscription import SubscriptionManager, SubscriptionPlan
import webbrowser
import os

def demo_subscription_cancellation():
    """Demo the subscription cancellation process"""
    
    print("=== Subscription Cancellation Demo ===\n")
    
    # Initialize subscription manager
    manager = SubscriptionManager()
    
    # Create some demo subscriptions
    print("Creating demo subscriptions...")
    sub1 = manager.create_subscription("user_001", SubscriptionPlan.PREMIUM)
    sub2 = manager.create_subscription("user_002", SubscriptionPlan.BASIC)
    sub3 = manager.create_subscription("user_003", SubscriptionPlan.ENTERPRISE)
    
    print(f"Created subscriptions:")
    print(f"1. {sub1.id} - {sub1.plan.value} (User: {sub1.user_id})")
    print(f"2. {sub2.id} - {sub2.plan.value} (User: {sub2.user_id})")
    print(f"3. {sub3.id} - {sub3.plan.value} (User: {sub3.user_id})")
    print()
    
    # Demo cancellation process
    print("Demo: Cancelling subscription via Python API")
    print("-" * 50)
    
    # Cancel first subscription
    success = manager.cancel_subscription(
        sub1.id, 
        "User requested cancellation via demo"
    )
    
    if success:
        print("✅ Subscription cancelled successfully!")
    else:
        print("❌ Failed to cancel subscription")
    
    print()
    
    # Show updated subscription status
    print("Updated subscription status:")
    cancelled_sub = manager.get_subscription(sub1.id)
    if cancelled_sub:
        print(f"Subscription {cancelled_sub.id}:")
        print(f"  Status: {cancelled_sub.status.value}")
        print(f"  Cancelled at: {cancelled_sub.cancelled_at}")
        print(f"  Reason: {cancelled_sub.cancellation_reason}")
    
    print()
    
    # Save subscriptions
    manager.save_to_file("demo_subscriptions.json")
    
    # Open web interface
    print("Opening web interface for subscription cancellation...")
    html_file = os.path.abspath("cancel_subscription.html")
    
    if os.path.exists(html_file):
        # Add subscription ID to URL for demo
        url = f"file://{html_file}?sub_id={sub2.id}"
        print(f"Opening: {url}")
        
        try:
            webbrowser.open(url)
            print("✅ Web interface opened in your default browser")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"Please manually open: {html_file}")
    else:
        print("❌ HTML file not found")
    
    print("\n=== Demo Complete ===")
    print("You can also run 'python subscription.py' for interactive CLI")

if __name__ == "__main__":
    demo_subscription_cancellation()