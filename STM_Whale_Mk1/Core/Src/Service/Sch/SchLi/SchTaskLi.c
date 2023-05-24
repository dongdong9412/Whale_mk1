
#include "SchTaskLi.h"

static vSchTask_cnt = 0;

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim){
	if (htim->Instance == TIM2){
		vSchTask_cnt++;
		if(vSchTask_cnt == 1000){		// 1 sec
			vSchTask_cnt = 0;
			HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
		}
	}
}
