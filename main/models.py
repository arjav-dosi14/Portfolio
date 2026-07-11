from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=100)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)
    board_or_university = models.CharField(max_length=200)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=50)
    percentage_or_cgpa = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.degree} from {self.institution_name}"
