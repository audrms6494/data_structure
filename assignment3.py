import time


### PROBLEM I ######################################################################################################
def solve_recursive_p1(N):
    """ 
    This function finds the number of cases satisfying the conditions using recursion.
    
    Args:
        N (int) : The number of students.
    
    Returns:
        (int) : The number of cases.
        
    """
    ### CODE HERE ###
    if N == 0 : # base - 아무도 자기의 핸드폰을 받지 않는 경우의 수는 사람이 없을 때 1이다.
        return 1
    elif N == 1 : # base - 한명의 사람, 하나의 휴대폰으로는 자신의 휴대폰을 피할 수 없다.
        return 0
    else : # 점화식 사용 (recursion)
        return (N-1) * (solve_recursive_p1(N-1) + solve_recursive_p1(N-2))
    #################


def solve_DP_p1(N):
    """ 
    This function find the number of cases satisfying the conditions using dynamic programming.
    
    Args:
        N (int) : The number of students.
    
    Returns:
       (int) : The number of cases.
       
    """
    ### CODE HERE ###
    dp = [1,0] # a_0 와 a_1
    for num in range(2,N+1) : # num이 2이상일 때
        ans = (num-1) * (dp[num-1] + dp[num-2]) # 점화식 사용 (dp)
        dp.append(ans)
    return dp[N]
    #################


def get_time_history_p1():
    """ 
    This function measures the runtimes of both algorithms and stores them in lists.   
    
    Args:
    
    Returns:
       (list) : Runtimes history of recursion.
       (list) : Runtimes history of dynamic programming.
       
    """
    
    time_history_recursive = []
    time_history_DP = []
    ### CODE HERE ###
    for num in range (30) : # recursion 함수의 시간 측정
        start = time.time()
        temp = solve_recursive_p1(num)
        runtime = time.time() - start
        time_history_recursive.append(runtime)
    for num in range (30) : # dp 함수의 시간 측정
        start = time.time()
        temp = solve_DP_p1(num)
        runtime = time.time() - start
        time_history_DP.append(runtime)
    #################
    return time_history_recursive, time_history_DP

####################################################################################################################


### PROBLEM II #####################################################################################################
def search_path_recursion(y, x):
    """ 
    This function finds the number of shortest paths to the target location using recursion.
    
    Args:
        y (int): y-coordinate of the target location.
        x (int): x-coordinate of the target location.
    
    Return:
        (int): The number of shortest paths to the target location.
    
    """
    ### CODE HERE ###
    if y == 1 or x == 1:  # base case
        return 1
    else:  # Recursive call
        return search_path_recursion(y-1, x) + search_path_recursion(y, x-1)
    #################
    
def solve_p2_recursion(n, m, k_coord=None):
    """ 
    This function finds the number of shortest paths when there is a stopover.
    
    Args:
        n (int): The number of rows. 
        m (int): The number of columns.
        k_coord (tuple): Coordinate of stopover
    
    Return:
        (int): The number of shortest paths.
    
    """
    ### CODE HERE ###
    a = k_coord[0]  # 서비스 센터의 좌표
    b = k_coord[1]
    # 서비스센터까지의 최단거리 + 서비스센터에서 집까지의 최단거리
    return search_path_recursion(a, b) * search_path_recursion(n-a+1, m-b+1)
    #################


def search_path_DP(y, x):
    """ 
    This function finds the number of shortest paths to the target location using dynamic programming.
    
    Args:
        y (int): y-coordinate of the target location.
        x (int): x-coordinate of the target location.
    
    Return:
        (int): The number of shortest paths.
    
    """
    ### CODE HERE ###
    dp = []
    for num in range(x*y):
        if num < y:  # base - 집의 좌표가 x == 1일 때
            dp.append(1)
        elif num % y == 0:  # base - 집의 좌표가 y == 1일때
            dp.append(1)
        else:
            dp.append(dp[num-y] + dp[num-1])  # dp method - 점화식 사용
    return dp[x*y-1]
    #################

def solve_p2_DP(n, m, k_coord=None):
    """ 
    This function finds the number of shortest paths when there is a stopover.
    
    Args:
        n (int): The number of rows. 
        m (int): The number of columns.
        k_coord (tuple): The coordinate of stopover. The elements of k_coord are integer.
    
    Return:
        (int): The number of shortest paths.
    
    """
    ### CODE HERE ###
    a = k_coord[0]
    b = k_coord[1]
    # 서비스센터까지의 최단거리 + 서비스센터에서 집까지의 최단거리
    return search_path_DP(a, b) * search_path_DP(n - a + 1, m - b + 1)
    #################

####################################################################################################################


### PROBLEM III ####################################################################################################
def solve_p3(num_coffee, labs, staff, robot):
    """ 
    This function finds the minimum cost of delivery.
    
    Args:
        num_coffee (int): Number of coffee. 
        labs (list): List of laboratories to receive the delivery.
        staff (int): Cost for using staff.
        robot (int): Cost for using robot.
    
    Return:
        (int): Minimum cost of delivery.
    
    """
    ### CODE HERE ###
    labs.sort()  # 오름차순으로 정렬
    sum_list = [labs[0]]  # sum_list[num] = labs[num] 까지 모든 값을 더한 값, sum_list[0] = labs[0]
    for num in range(1, num_coffee):  # sum_list[num] = labs[num] + sum_list[num-1]
        sum_list.append(labs[num] + sum_list[num - 1])
    lst_dist = [[0] * num_coffee for num in range(num_coffee)]  # 2차원 배열 생성
    for m in range(num_coffee):  # lst_dist[n][m] = labs의 n번째 요소부터 m번째 요소까지 중간값까지의 최단거리
        # n == 0 일 때
        if m % 2 == 0:  # m - 0이 짝수일 때 -> 0~m까지의 요소의 개수인 m+1이 홀수일 때
            lst_dist[0][m] = sum_list[m] - 2 * sum_list[m // 2] + labs[m // 2]  
        else:  # m - 0이 홀수일 때 -> 0~m까지의 요소의 개수인 m+1이 짝수일 때
            lst_dist[0][m] = sum_list[m] - 2 * sum_list[m // 2]
        for n in range(1, m):  # n != 0일 때
            if (m - n) % 2 == 0:  # m-n이 짝수일 때 -> n~m까지의 요소의 개수인 m-n+1이 홀수일 때
                lst_dist[n][m] = sum_list[m] + sum_list[n - 1] - 2 * sum_list[(m + n) // 2] + labs[(m + n) // 2]
            else:  # m-n이 홀수일 때 -> n~m까지의 요소의 개수인 m-n+1이 짝수일 때
                lst_dist[n][m] = sum_list[m] + sum_list[n - 1] - 2 * sum_list[(m + n) // 2]
    dp = [0] * num_coffee  # dp[k] = k번째 index까지 최소비용
    for k in range(num_coffee):
        dp[k] = labs[k] * staff + dp[k - 1]  # 스태프를 이용할 때
        for n in range(k):  # 로봇을 사용할 때
            if dp[n] + robot + staff * lst_dist[n + 1][k] < dp[k]:  # 사용하는 그 로봇을 쓰는 lab의 범위 설정
                dp[k] = dp[n] + robot + staff * lst_dist[n + 1][k]  # 비용이 미리 들어가있는 비용보다 적을 때 그 비용 입력
    return dp[num_coffee - 1]  # 최소비용 반환
    
    #################

####################################################################################################################
