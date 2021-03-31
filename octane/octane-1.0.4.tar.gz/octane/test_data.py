import octane

meter = octane.Meter.create(name="num_video_sessions", display_name="Number of Video Sessions", meter_type="counter", is_incremental=True)

price_plan = octane.PricePlan(name="basic_price_plan", display_name="Basic Price Plan", period="month", metered_components=[{"meter_name": "num_video_sessions", "price_scheme": {}}])
