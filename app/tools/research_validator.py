from collections import Counter
from app.schemas.research import (ResearchTaskPlan, TaskType)

class ResearchPlanValidator:

    def validate(self, plan: ResearchTaskPlan) -> ResearchTaskPlan:
        self.validate_task_types(plan)
        self.validate_dependencies(plan)
        self.validate_required_inputs(plan)
        self.validate_task_order(plan)

        return plan

    def validate_task_types(self, plan: ResearchTaskPlan) -> None:
        """
        Ensure that every task uses a supported task type.
        """

        allowed_types = {
            TaskType.COMPANY_IDENTIFICATION,
            TaskType.FINANCIAL_DATA,
            TaskType.FINANCIAL_ANALYSIS,
            TaskType.RISK_ANALYSIS,
        }

        for task in plan.tasks:
            if task.task_type not in allowed_types:
                raise ValueError(
                    f"Unsupported task type '{task.task_type}' "
                    f"for task '{task.task_id}'"
                )

    def validate_dependencies(self, plan: ResearchTaskPlan) -> None:
        """
        Ensure that dependencies:
        - reference existing tasks
        - don't reference themselves
        - don't contain duplicates
        """

        task_ids = {task.task_id for task in plan.tasks}

        for task in plan.tasks:

            if task.task_id in task.depends_on:
                raise ValueError(
                    f"Task '{task.task_id}' cannot depend on itself."
                )

            duplicate_dependencies = [
                dep
                for dep, count in Counter(task.depends_on).items()
                if count > 1
            ]

            if duplicate_dependencies:
                raise ValueError(
                    f"Task '{task.task_id}' contains duplicate dependencies: "
                    f"{duplicate_dependencies}"
                )

            for dependency in task.depends_on:

                if dependency not in task_ids:
                    raise ValueError(
                        f"Task '{task.task_id}' depends on unknown task "
                        f"'{dependency}'."
                    )

    def validate_required_inputs(self, plan: ResearchTaskPlan) -> None:
        """
        Ensure each task type contains the inputs required
        to execute that type of task.
        """

        for task in plan.tasks:

            if task.task_type == TaskType.COMPANY_IDENTIFICATION:

                if not task.inputs.get("company_name"):
                    raise ValueError(
                        f"Company identification task '{task.task_id}' "
                        f"requires 'company_name'."
                    )

            elif task.task_type == TaskType.FINANCIAL_DATA:

                if not task.inputs.get("company"):
                    raise ValueError(
                        f"Financial data task '{task.task_id}' "
                        f"requires 'company'."
                    )

                if not task.inputs.get("metrics"):
                    raise ValueError(
                        f"Financial data task '{task.task_id}' "
                        f"requires 'metrics'."
                    )

                if not task.inputs.get("period"):
                    raise ValueError(
                        f"Financial data task '{task.task_id}' "
                        f"requires 'period'."
                    )

            elif task.task_type == TaskType.FINANCIAL_ANALYSIS:

                if not task.inputs.get("financial_data"):
                    raise ValueError(
                        f"Financial analysis task '{task.task_id}' "
                        f"requires 'financial_data'."
                    )

            elif task.task_type == TaskType.RISK_ANALYSIS:

                if not task.inputs.get("financial_data"):
                    raise ValueError(
                        f"Risk analysis task '{task.task_id}' "
                        f"requires 'financial_data'."
                    )

    def validate_task_order(self, plan: ResearchTaskPlan) -> None:
        """
        Ensure dependencies appear before the task that depends on them.
        """

        task_position = {
            task.task_id: index
            for index, task in enumerate(plan.tasks)
        }

        for task in plan.tasks:

            current_position = task_position[task.task_id]

            for dependency in task.depends_on:

                dependency_position = task_position[dependency]

                if dependency_position >= current_position:
                    raise ValueError(
                        f"Task '{task.task_id}' depends on "
                        f"'{dependency}', but '{dependency}' does not "
                        f"appear before it in the research plan."
                    )