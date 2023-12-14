customer_id = User.objects.filter(id=1).first()
university = University.objects.filter(id=1600).first()
direction = Direction.objects.filter(id=3400).first()
course = Course.objects.filter(id=10).first()
Task(customer_id=customer_id, is_done=False, is_working=False, title="123", description="sad", university=university,
     direction=direction,
     course=course).save()